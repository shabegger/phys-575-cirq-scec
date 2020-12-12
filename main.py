from qubit import LogicalQubit

logicalQubit = LogicalQubit(2, 0.05)
logicalQubit.applyX()

results = logicalQubit.run()
print(results.measurements)
# for i in results.final_state_vector:
#     print(i)
# logicalQubit.print()

for i in range(100):
    count = 0
