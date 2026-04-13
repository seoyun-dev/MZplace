#!/usr/bin/env python3
import csv
import math
import random
from collections import defaultdict


def load_hearts(path):
    interactions = []
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user_id = row['user_id'].strip()
            place_id = row['place_id'].strip()
            created_at = row.get('created_at', '').strip()
            if user_id and place_id:
                interactions.append((user_id, place_id, created_at))
    return interactions


def train_test_split_leave_one_out(interactions):
    by_user = defaultdict(list)
    for user_id, place_id, created_at in interactions:
        by_user[user_id].append((created_at, place_id))

    train = []
    test = []

    for user_id, rows in by_user.items():
        if len(rows) < 2:
            continue
        rows.sort(key=lambda x: x[0])
        test_item = rows[-1][1]
        train_items = [place_id for _, place_id in rows[:-1]]
        for place_id in train_items:
            train.append((user_id, place_id))
        test.append((user_id, test_item))

    return train, test


def build_interaction_sets(train):
    user_to_items = defaultdict(set)
    item_to_users = defaultdict(set)
    for user_id, place_id in train:
        user_to_items[user_id].add(place_id)
        item_to_users[place_id].add(user_id)
    return user_to_items, item_to_users


def jaccard_similarity(set_a, set_b):
    if not set_a or not set_b:
        return 0.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union else 0.0


def cosine_similarity(set_a, set_b):
    if not set_a or not set_b:
        return 0.0
    intersection = len(set_a & set_b)
    return intersection / math.sqrt(len(set_a) * len(set_b)) if len(set_a) and len(set_b) else 0.0


def compute_user_similarity(user_to_items):
    users = list(user_to_items.keys())
    similarities = {}
    for i, user_i in enumerate(users):
        items_i = user_to_items[user_i]
        for user_j in users[i:]:
            items_j = user_to_items[user_j]
            score = jaccard_similarity(items_i, items_j)
            similarities[(user_i, user_j)] = score
            similarities[(user_j, user_i)] = score
    return similarities


def compute_item_similarity(item_to_users):
    items = list(item_to_users.keys())
    similarities = {}
    for i, item_i in enumerate(items):
        users_i = item_to_users[item_i]
        for item_j in items[i:]:
            users_j = item_to_users[item_j]
            score = cosine_similarity(users_i, users_j)
            similarities[(item_i, item_j)] = score
            similarities[(item_j, item_i)] = score
    return similarities


def ubcf_candidate_scores(user_id, user_to_items, item_to_users, user_similarity, all_items):
    # UBCF 점수 계산
    # 각 후보 장소에 대해 해당 장소를 찜한 다른 사용자들과 현재 사용자의 유사도를 합산
    # 이 점수가 높을수록 현재 사용자와 취향이 비슷한 사용자들이 많이 찜한 장소라는 뜻
    seen = user_to_items.get(user_id, set())
    scores = {}
    for item in all_items:
        if item in seen:
            continue
        candidate_users = item_to_users.get(item, set())
        score_sum = 0.0
        for other_user in candidate_users:
            if other_user == user_id:
                continue
            score_sum += user_similarity.get((user_id, other_user), 0.0)
        if score_sum > 0.0:
            scores[item] = score_sum
    return scores


def ibcf_candidate_scores(user_id, user_to_items, item_similarity, all_items):
    # IBCF 점수 계산
    # 후보 장소와 사용자가 찜한 장소 간의 유사도를 합산
    # 이 점수가 높을수록 사용자가 좋아한 장소와 비슷한 후보라는 뜻
    seen = user_to_items.get(user_id, set())
    scores = {}
    for item in all_items:
        if item in seen:
            continue
        score_sum = 0.0
        for liked_item in seen:
            if liked_item == item:
                continue
            score_sum += item_similarity.get((item, liked_item), 0.0)
        if score_sum > 0.0:
            scores[item] = score_sum
    return scores


def top_k_from_scores(scores, k=10):
    # score가 높은 순서대로 정렬 후 상위 k개 candidate를 반환
    ordered = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [item for item, _ in ordered[:k]]


def hybrid_candidate_scores(ubcf_scores, ibcf_scores, alpha):
    # UBCF와 IBCF 점수를 정규화한 뒤 alpha 가중치로 결합
    # alpha=1.0이면 UBCF만 사용, alpha=0.0이면 IBCF만 사용
    max_ubcf = max(ubcf_scores.values(), default=1.0)
    max_ibcf = max(ibcf_scores.values(), default=1.0)
    hybrid_scores = {}
    for item in set(ubcf_scores) | set(ibcf_scores):
        ubcf_norm = ubcf_scores.get(item, 0.0) / max_ubcf
        ibcf_norm = ibcf_scores.get(item, 0.0) / max_ibcf
        score = alpha * ubcf_norm + (1.0 - alpha) * ibcf_norm
        if score > 0.0:
            hybrid_scores[item] = score
    return hybrid_scores


def compute_metrics_for_recommendations(test_items, user_to_items_train, recommendations, k):
    # 평가 지표 계산
    # Precision@K: hit/k 누적
    # Recall@K: hit 개수 / 전체 테스트 사용자 수
    # NDCG@K: 추천 순위 품질을 반영
    metrics = {'hit': 0, 'precision': 0.0, 'ndcg': 0.0, 'count': 0}
    for user_id, true_item in test_items:
        if user_id not in user_to_items_train:
            continue
        metrics['count'] += 1
        rec_items = recommendations.get(user_id, [])[:k]
        hit = 1 if true_item in rec_items else 0
        metrics['hit'] += hit
        metrics['precision'] += hit / k
        if hit:
            rank = rec_items.index(true_item) + 1
            metrics['ndcg'] += 1.0 / math.log2(rank + 1)
    return metrics


def evaluate_recommender(test_items, user_to_items_train, all_items, user_similarity, item_similarity, item_to_users, k=10, alpha=0.5, top_n=50):
    # 상위 top_n 후보를 생성하고, 그 후보군을 가지고 K 기준 평가 수행
    # top_n=50이므로 최대 50개의 추천 후보를 만든 뒤 K 개로 끊어서 측정
    ubcf_recommendations = {}
    ibcf_recommendations = {}
    hybrid_recommendations = {}

    for user_id, _ in test_items:
        if user_id not in user_to_items_train:
            continue
        ubcf_scores = ubcf_candidate_scores(user_id, user_to_items_train, item_to_users, user_similarity, all_items)
        ibcf_scores = ibcf_candidate_scores(user_id, user_to_items_train, item_similarity, all_items)
        hybrid_scores = hybrid_candidate_scores(ubcf_scores, ibcf_scores, alpha)

        ubcf_recommendations[user_id] = top_k_from_scores(ubcf_scores, top_n)
        ibcf_recommendations[user_id] = top_k_from_scores(ibcf_scores, top_n)
        hybrid_recommendations[user_id] = top_k_from_scores(hybrid_scores, top_n)

    result = {}
    for mode_name, recommendations in [('ubcf', ubcf_recommendations), ('ibcf', ibcf_recommendations), ('hybrid', hybrid_recommendations)]:
        metrics = compute_metrics_for_recommendations(test_items, user_to_items_train, recommendations, k)
        count = metrics['count']
        if count == 0:
            result[mode_name] = {
                'count': 0,
                'precision@{}'.format(k): 0.0,
                'recall@{}'.format(k): 0.0,
                'ndcg@{}'.format(k): 0.0,
            }
            continue
        result[mode_name] = {
            'count': count,
            'precision@{}'.format(k): metrics['precision'] / count,
            'recall@{}'.format(k): metrics['hit'] / count,
            'ndcg@{}'.format(k): metrics['ndcg'] / count,
        }
    return result


def write_results_csv(path, rows, fieldnames):
    with open(path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_results_markdown(path, rows, columns, title=None):
    with open(path, 'w', encoding='utf-8') as mdfile:
        if title:
            mdfile.write(f'# {title}\n\n')
        mdfile.write('| ' + ' | '.join(columns) + ' |\n')
        mdfile.write('| ' + ' | '.join('---' for _ in columns) + ' |\n')
        for row in rows:
            mdfile.write('| ' + ' | '.join(str(row.get(c, '')) for c in columns) + ' |\n')


def format_table(rows, columns):
    widths = []
    for c in columns:
        max_width = len(c)
        for row in rows:
            max_width = max(max_width, len(str(row.get(c, ''))))
        widths.append(max_width)
    sep = ' | '
    header = sep.join(c.ljust(w) for c, w in zip(columns, widths))
    divider = '-+-'.join('-' * w for w in widths)
    lines = [header, divider]
    for row in rows:
        lines.append(sep.join(str(row.get(c, '')).ljust(w) for c, w in zip(columns, widths)))
    return '\n'.join(lines)


def find_best_alpha(alpha_results, k, metric_key):
    best_alpha = None
    best_value = -1.0
    for alpha, ks_results in alpha_results.items():
        value = ks_results[k]['hybrid'][metric_key]
        if value > best_value:
            best_value = value
            best_alpha = alpha
    return best_alpha, best_value


def main():
    # 데이터 로딩 및 사용자-장소 행렬 구성
    interactions = load_hearts('places/hearts_data.csv')
    train, test = train_test_split_leave_one_out(interactions)
    user_to_items, item_to_users = build_interaction_sets(train)
    all_items = sorted(item_to_users.keys())
    user_similarity = compute_user_similarity(user_to_items)
    item_similarity = compute_item_similarity(item_to_users)

    ks = [10, 20, 50]
    alphas = [round(x * 0.1, 1) for x in range(11)]

    print('\nRecommender evaluation results:')
    print('  train interactions:', len(train))
    print('  test interactions:', len(test))

    baseline_rows = []
    for k in ks:
        results = evaluate_recommender(test, user_to_items, all_items, user_similarity, item_similarity, item_to_users, k=k)
        for mode, result in results.items():
            baseline_rows.append({
                'K': k,
                'Model': mode.upper(),
                'Precision': '{:.4f}'.format(result[f'precision@{k}']),
                'Recall': '{:.4f}'.format(result[f'recall@{k}']),
                'NDCG': '{:.4f}'.format(result[f'ndcg@{k}']),
            })

    print('\nBaseline metrics (alpha=0.5 hybrid):')
    print(format_table(baseline_rows, ['K', 'Model', 'Precision', 'Recall', 'NDCG']))
    write_results_csv('evaluation_results.csv', baseline_rows, ['K', 'Model', 'Precision', 'Recall', 'NDCG'])
    write_results_markdown('evaluation_results.md', baseline_rows, ['K', 'Model', 'Precision', 'Recall', 'NDCG'], title='Baseline Evaluation Metrics')

    alpha_rows = []
    alpha_eval = {}
    for alpha in alphas:
        alpha_eval[alpha] = {}
        for k in ks:
            alpha_eval[alpha][k] = evaluate_recommender(test, user_to_items, all_items, user_similarity, item_similarity, item_to_users, k=k, alpha=alpha)
            alpha_rows.append({
                'Alpha': alpha,
                'K': k,
                'Precision': '{:.4f}'.format(alpha_eval[alpha][k]['hybrid'][f'precision@{k}']),
                'Recall': '{:.4f}'.format(alpha_eval[alpha][k]['hybrid'][f'recall@{k}']),
                'NDCG': '{:.4f}'.format(alpha_eval[alpha][k]['hybrid'][f'ndcg@{k}']),
            })

    write_results_csv('hybrid_alpha_search.csv', alpha_rows, ['Alpha', 'K', 'Precision', 'Recall', 'NDCG'])
    write_results_markdown('hybrid_alpha_search.md', alpha_rows, ['Alpha', 'K', 'Precision', 'Recall', 'NDCG'], title='Hybrid Alpha Search Results')

    print('\nHybrid alpha search results:')
    for k in ks:
        best_alpha, best_ndcg = find_best_alpha(alpha_eval, k, f'ndcg@{k}')
        print(f'  Best alpha for NDCG@{k}: {best_alpha} (ndcg={best_ndcg:.4f})')

    print('\nSaved files: evaluation_results.csv, evaluation_results.md, hybrid_alpha_search.csv, hybrid_alpha_search.md')
    print('\nNotes:')
    print('  - UBCF: 사용자 기반 협업 필터링')
    print('  - IBCF: 항목 기반 협업 필터링')
    print('  - Hybrid: UBCF와 IBCF 점수를 alpha*(UBCF_norm) + (1-alpha)*(IBCF_norm) 방식으로 결합')
    print('  - precision@K: 추천 상위 K개 중 실제 정답 비율')
    print('  - recall@K: 추천 상위 K개에 실제 정답이 포함될 확률')
    print('  - ndcg@K: 추천 순위까지 반영하는 순위 기반 지표')

if __name__ == '__main__':
    main()
