x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

if y1 + y2 == 0:
    # rare case, line AB' parallel to x-axis => no finite P unless y1=0
    if y1 == 0:
        x = x1
    else:
        # but problem will not give this
        x = (x1 + x2) / 2  # fallback
else:
    x = x1 + y1 * (x2 - x1) / (y1 + y2)

print(f"{x:.10f} 0.0000000000")