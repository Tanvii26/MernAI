import pandas as pd
import math
from sklearn.metrics.pairwise import cosine_similarity
from app.utils import profile_score, relevancy_score, sentence_model

def process_matching(experts_df, candidates_df, interview_subject):
    """Compute relevancy score between experts and candidates."""

    experts = experts_df.to_dict(orient='records')
    # candidates = candidates_df.to_dict(orient='records')
    # Get expert skills embeddings
    expert_skills = [expert['skills'] for expert in experts]
    expert_embeddings = sentence_model.encode(expert_skills)
    
    # Get subject embedding
    subject_embedding = sentence_model.encode([interview_subject])
    
    # Compute matching scores between experts and the subject
    matching_scores = cosine_similarity(expert_embeddings, subject_embedding)
    
    # Assign matching scores to experts
    for idx, expert in enumerate(experts):
        expert['matching_score'] = matching_scores[idx][0]

    # Create DataFrame for ranking
    experts_df = pd.DataFrame(experts)
    
    # Filter experts by availability
    experts_df = experts_df[experts_df['date_of_availability'] == '2024-09-15']
    experts_df = experts_df[experts_df['matching_score'] > 0]

    # Sort and select top experts
    top_experts = experts_df.sort_values(by='matching_score', ascending=False).head(10)
    
    # Calculate profile scores and relevancy scores
    allocations = {expert['name']: [] for _, expert in top_experts.iterrows()}  # To store allocated candidates
    remaining_candidates = candidates_df.copy()  # Copy to track unallocated candidates
    threshold = math.ceil(len(candidates_df) / len(top_experts))

    for _, expert in top_experts.iterrows():
        expert_name = expert['name']
        # Calculate the relevancy score for each candidate
        candidate_scores = []
        for _, candidate in remaining_candidates.iterrows():
            score = profile_score(expert, candidate)
            candidate_scores.append({
                'Candidate': candidate['name'],
                'Relevancy Score': score
            })

        # Sort candidates by the relevancy score in descending order
        sorted_candidates = sorted(candidate_scores, key=lambda x: x['Relevancy Score'], reverse=True)

        # Allot top 'threshold' candidates to the expert
        allocated_candidates = sorted_candidates[:threshold]
        allocations[expert_name].extend(allocated_candidates)

        # Remove allocated candidates from the remaining pool
        remaining_candidates = remaining_candidates[~remaining_candidates['name'].isin([c['Candidate'] for c in allocated_candidates])]

    return allocations
