# /python-service/app/model.py
import torch
from transformers import BertTokenizer, BertModel
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load the pre-trained Sentence-BERT model once
sentence_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Function to get sentence embeddings
def get_embeddings(text_list):
    embeddings = sentence_model.encode(text_list)
    return embeddings

# Function to compute cosine similarity between two sets of embeddings
def compute_similarity(expert_embeddings, subject_embedding):
    return cosine_similarity(expert_embeddings, [subject_embedding])

def profile_score(expert_skills, candidate_skills):
    # Get embeddings for expert and candidate skills
    expert_embed = get_embeddings([expert_skills])[0]
    candidate_embed = get_embeddings([candidate_skills])[0]

    # Compute cosine similarity between expert and candidate
    skill_score = cosine_similarity([expert_embed], [candidate_embed])[0][0]
    return skill_score
