import pandas as pd
import numpy as np
from scipy.stats import mode
from sklearn.metrics import f1_score
from sklearn.metrics import jaccard_score
from sklearn.model_selection import train_test_split



######## 각 행 간의 Jaccard 유사도 계산
def calculate_jaccard_similarity(matrix):
    num_users = matrix.shape[0]
    similarities = np.zeros((num_users, num_users))

    for i in range(num_users):
        for j in range(i, num_users):
            similarity = jaccard_score(matrix.iloc[i], matrix.iloc[j])
            similarities[i, j] = similarity
            similarities[j, i] = similarity

    return similarities


######## 평점(1/0)을 예측하는 함수
def cf_binary(user_id, place_id):
    if place_id in likes_matrix:
        sim_scores     = user_similarity[user_id].copy()
        place_likes    = likes_matrix[place_id].copy()
        none_likes_idx = place_likes[place_likes.isnull()].index
        place_likes    = place_likes.drop(none_likes_idx)
        sim_scores     = sim_scores.drop(none_likes_idx)

        if sim_scores.sum() != 0.0:
            predicted_likes = np.dot(sim_scores, place_likes) / sim_scores.sum()
        else:
            predicted_likes = mode(place_likes, keepdims=True).mode[0]
            #predicted_likes = 0.0

    else:
        predicted_likes = 0.0 # 특정 장소에 대한 좋아요 없는 경우 예측 불가

    return predicted_likes


######## 추천하는 장소 id 반환하는 함수
def recommender(user, n_items):
    #현재 사용자의 모든 아이템에 대한 예상 평점 계산
    predictions = []
    liked_index = likes_matrix.loc[user][likes_matrix.loc[user] > 0].index    # 이미 찜하기 누른 장소 인덱스 가져옴
    #print("liked_index", liked_index)
    items = likes_matrix.loc[user].drop(liked_index) # 찜하기 누른 장소 제외하고 추천하기 위해
    #print(items)
    
    for item in items.index:
        predictions.append(cf_binary(user, item))                   # 예상 1, 0계산
    recommendations = pd.Series(data=predictions, index=items.index, dtype=float)
    recommendations = recommendations.sort_values(ascending=False)[:n_items]    
    recommendations = recommendations[recommendations==1.0]
    return recommendations


############# 실행할 함수
def recommend_places(user_id, n_items):
    # 52번 사용자에게 추천할 장소
    # 최대 장소 10개 가져오도록
    # print(recommender(user=52, n_items=10))
    return recommender(user=user_id, n_items=20)



####### 데이터 정제하여 유사도 계산
likes = pd.read_csv('/Users/seoyun/Desktop/team_projects/mz/places/hearts_data.csv', encoding='UTF-8-SIG')
likes = likes[["place_id", "user_id"]]
likes.loc[:, "heart"] = 1
likes = likes.drop_duplicates(subset=['place_id', 'user_id'], keep='first') # 중복 하트 제거

x = likes.copy()
y = likes['user_id']

# train, test 분리
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, stratify=y)

# 전체 데이터로 full matrix와 자가드 유사도 구하기 
likes_matrix    = likes.pivot_table(index='user_id', columns='place_id', values='heart')
matrix_dummy    = likes_matrix.copy().fillna(0)
user_similarity = calculate_jaccard_similarity(matrix_dummy)
user_similarity = pd.DataFrame(user_similarity, index=likes_matrix.index, columns=likes_matrix.index)

print(recommend_places(1, 20))
