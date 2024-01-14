export PYTHONPATH=.:$PYTHONPATH

python scripts/solve_competition.py \
    --file_name ./data/TAL-SAQ6K-EN.jsonl \
    --save_name ./results/TAL_SAQ6K_EN_prediction.json \
    --max_evaluate_times 15 \
    --if_retrieval True \
    --llm gpt-4-1106-preview \
