import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from transformers import BertTokenizer, BertModel
import torch

# Load Sentence-BERT model
sentence_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Initialize BERT model and tokenizer
bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert_model = BertModel.from_pretrained('bert-base-uncased')

def get_bert_embeddings(text):
    """Get BERT embeddings for a given text."""
    inputs = bert_tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        outputs = bert_model.forward(**inputs)
    embeddings = outputs.last_hidden_state
    attention_mask = inputs['attention_mask']
    mask = attention_mask.unsqueeze(-1).expand(embeddings.size()).float()
    masked_embeddings = embeddings * mask
    summed = torch.sum(masked_embeddings, 1)
    summed_mask = torch.clamp(mask.sum(1), min=1e-9)
    mean_pooled = summed / summed_mask
    return mean_pooled.numpy()

def profile_score(expert, candidate):
    """Calculate profile score between expert and candidate."""
    # Simple string matching for qualifications
    
    qual_score = 1 if expert['qualifications'] in candidate['qualifications'] else 0
    
    # Experience comparison
    exp_diff = abs(expert['years_of_experience'] - candidate['years_of_experience'])
    exp_score = 1 / (1 + exp_diff)
    
    # Skills similarity (using BERT embeddings)
    expert_embed = get_bert_embeddings(expert['skills'])
    candidate_embed = get_bert_embeddings(candidate['skills'])
    skill_score = cosine_similarity(expert_embed, candidate_embed)[0][0]

    # Final weighted score
    return 0.3 * qual_score + 0.3 * exp_score + 0.4 * skill_score

def relevancy_score(matching_score, profile_score):
    """Calculate the final relevancy score."""
    return 0.5 * matching_score + 0.5 * profile_score
