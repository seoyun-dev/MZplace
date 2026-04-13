# Recommendation Evaluation Summary

## 1. 실험 데이터셋
- 사용 데이터: `places/hearts_data.csv`
- 데이터 출처: 프로젝트 내 찜(Heart) 로그 CSV 파일
- 데이터 구성:
  - `user_id`: 사용자 식별자
  - `place_id`: 장소 식별자
  - `created_at`: 찜 생성 시각
- 평가 방식: 각 사용자마다 가장 최신 찜 1개를 테스트 데이터로 떼고, 나머지를 학습 데이터로 사용하는 Leave-One-Out 방식
- 실제 학습/테스트 크기: 804개 학습 인터랙션, 60개 테스트 인터랙션

## 2. 모델 구성
### UBCF (User-Based Collaborative Filtering)
- 사용자 간 유사도를 계산하여 추천
- 유사도: `Jaccard`
- 추천 점수: 후보 장소를 찜한 다른 사용자들의 유사도 합

### IBCF (Item-Based Collaborative Filtering)
- 아이템(장소) 간 유사도를 계산하여 추천
- 유사도: `Cosine`
- 추천 점수: 후보 장소와 사용자가 찜한 장소들의 유사도 합

### Hybrid
- UBCF 점수와 IBCF 점수를 섞은 하이브리드
- 공식: `score = alpha * UBCF_norm + (1 - alpha) * IBCF_norm`
- 여기서 `alpha`는 결합 가중치
- `UBCF_norm`, `IBCF_norm`는 각각 0~1 사이로 정규화된 점수

## 3. 평가 지표
### Precision@K
- 추천 상위 K개 항목 중 실제 정답(테스트 아이템)이 포함된 비율
- 사용자 입장에서 추천 결과의 정확도를 보는 지표
- **높을수록 좋음**: 추천된 항목 중 실제 관심 있는 비율이 높아야 좋은 추천

### Recall@K
- 실제 정답이 추천 상위 K개에 들어갈 확률
- 중요한 아이템을 놓치지 않는지를 보는 지표
- **높을수록 좋음**: 사용자가 관심 있을 만한 아이템을 최대한 많이 추천해야 좋음

### NDCG@K
- 추천 순위까지 반영한 순위 기반 지표
- 정답이 상위에 있을수록 더 높은 점수를 부여
- 추천 결과의 순서 품질을 평가할 때 사용함
- **높을수록 좋음**: 정답 아이템이 상위에 위치할수록 점수가 높아짐

### K의 실제 의미와 코드 동작
- `K`는 평가할 추천 리스트 길이입니다.
- 본 평가에서는 `K=50`을 사용하여 상위 50개 추천 리스트 전체를 평가합니다.
- 실제 코드에서는 먼저 후보 아이템을 상위 50개(`top_n=50`)까지 뽑고, 그 전체를 `K=50`으로 평가합니다.

## 4. 목표 지표별 튜닝이란?
- `alpha`는 hybrid 모델에서 UBCF와 IBCF를 얼마나 섞을지 결정하는 값
- 목표 지표별 튜닝은 다음 의미:
  - `precision`을 주요 목표로 하면 precision이 가장 좋은 alpha를 선택
  - `recall`을 주요 목표로 하면 recall이 가장 좋은 alpha를 선택
  - `ndcg`를 주요 목표로 하면 추천 순위 품질을 가장 잘 만족하는 alpha를 선택
- 즉, 서비스 목표에 따라 alpha를 다르게 정하는 방식이다
  - 검색 중심 추천: `Precision` 우선
  - 탐색성/발견성 중심 추천: `Recall` 우선
  - 순위 품질이 중요한 추천: `NDCG` 우선

## 5. 서비스 코드와 평가 코드 차이
- 현재 `places/views.py` 실제 서비스 코드에서는 UBCF/IBCF 점수를 정규화한 뒤 best alpha=0.8로 결합한 **score fusion**을 사용합니다.
- 평가 코드에서도 동일한 score fusion 방식을 사용하여 성능을 비교했습니다.
- 공식: `score = 0.8 * UBCF_norm + 0.2 * IBCF_norm`

## 6. 결과표 위치
- 베이스라인 결과: `evaluation_results.md`
- Hybrid alpha 탐색 결과: `hybrid_alpha_search.md`

## 7. 주요 결과 요약
### Baseline (alpha=0.5 hybrid)
| K | UBCF Recall@50 | IBCF Recall@50 | Hybrid Recall@50 |
|---|----------------|----------------|------------------|
| 50 | 0.4833 | 0.3833 | 0.4500 |

### Alpha 탐색 결과 (현재는 NDCG 기준 최적값)
- `K=50`: best alpha = 0.8

### best alpha 적용 결과
| K | best alpha | Precision@50 | Recall@50 | NDCG@50 |
|---|------------|--------------|-----------|---------|
| 50 | 0.8 | 0.0100 | 0.5000 | 0.1912 |

### best alpha일 때 UBCF / IBCF / Hybrid 성능 비교
| Model | Alpha | Precision@50 | Recall@50 | NDCG@50 |
|---|---|---|---|---|
| UBCF | — | 0.0097 | 0.4833 | 0.1850 |
| IBCF | — | 0.0077 | 0.3833 | 0.1577 |
| Hybrid | 0.8 | 0.0100 | 0.5000 | 0.1912 |

### 이걸 적용하면 되나?
- 목표 지표를 `NDCG`로 정했다면 위 alpha 값을 적용한 hybrid가 현재 가장 좋은 결과를 냅니다.
- 다만, 서비스 목표가 `Precision`이나 `Recall`일 경우에는 해당 지표 기준으로 alpha를 다시 탐색해야 합니다.
- 따라서 최종 평가는 다음 절차로 진행하는 것이 좋습니다
  1. 서비스 목표 지표 선택(`Precision`, `Recall`, `NDCG` 중 하나 또는 복수)
  2. 그 지표 기준으로 alpha 값을 탐색
  3. 최적 alpha로 hybrid 모델을 구성하고 `K=10/20/50` 등으로 평가

## 7. 왜 이 지표를 선택했나?
- `Precision@K`: 추천 상위 결과의 정확도를 직접적으로 보여줌
- `Recall@K`: 사용자가 좋아할 가능성이 있는 아이템을 놓치지 않는지를 평가함
- `NDCG@K`: 단순 포함 여부가 아니라 순위까지 고려해 추천 품질을 더 정교하게 봄

