def preprocess_history(history, contracts, nurses):
    for nurse_id in history:
        history[nurse_id]['num_cons_shift'] = min(history[nurse_id]['num_cons_shift'], contracts[nurses[nurse_id]['contract_type']]['max_cons_working_days'])
    return history