from bayes_opt import BayesianOptimization, acquisition

acq = acquisition.UpperConfidenceBound(kappa=2.5)

# Define the search space (using a dictionary for bounds)
pbounds = {
    'learning_rate': (0, 7),  # Indices for categorical values (0 to 7)
    'batch_size': (0, 3),      # Indices for categorical values (0 to 1)
}

# Define the actual categorical values (lists)
learning_rates = [2e-6, 5e-6, 1e-5, 2e-5, 3e-5, 5e-5, 1e-4, 2e-4]
batch_sizes = [4, 8, 12, 16]

# Initialize the optimizer
optimizer = BayesianOptimization(
    f=None, 
    acquisition_function=acq,
    pbounds=pbounds,
    verbose=2,
    random_state=42,
    allow_duplicate_points=True,
)

# Add previous trials
previous_trials = [
    ([5e-5, 16], -0.1429109424352646),
    ([2e-6, 4], -0.17977488040924072),
    ([1e-4, 16], -0.13980011641979218),
    ([2e-4, 4], -0.1539500504732132),
    ([2e-4, 16], -0.1400434821844101),
    ([1e-4, 12], -0.14113132655620575),
    ([2e-4, 12], -0.1405016928911209),
]

for params, loss in previous_trials1:
    target = loss
    learning_rate_index = learning_rates.index(params[0])
    batch_size_index = batch_sizes.index(params[1])
    current_params = {'learning_rate': learning_rate_index, 'batch_size': batch_size_index}
    optimizer.register(
        params=current_params,
        target=target,
    )
    print("Found the target value to be:", target)

    next_point_to_probe = optimizer.suggest()

    # Convert indices to actual hyperparameter values
    suggested_learning_rate_index = int(round(next_point_to_probe['learning_rate']))
    suggested_batch_size_index = int(round(next_point_to_probe['batch_size']))

    suggested_learning_rate = learning_rates[suggested_learning_rate_index]
    suggested_batch_size = batch_sizes[suggested_batch_size_index]

    print("Next point to probe (converted):", {'learning_rate': suggested_learning_rate, 'batch_size': suggested_batch_size})

print(optimizer.max)

# Convert best parameters to actual values
best_params_indices = optimizer.max['params']
best_learning_rate = learning_rates[int(round(best_params_indices['learning_rate']))]
best_batch_size = batch_sizes[int(round(best_params_indices['batch_size']))]

print("Best parameters (converted):", {'learning_rate': best_learning_rate, 'batch_size': best_batch_size}, "Best Loss:", optimizer.max['target'])