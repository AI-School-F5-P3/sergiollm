import torch
print(torch.cuda.is_available())  # Verifica si CUDA está disponible
print(torch.cuda.device_count())  # Verifica cuántas GPUs están disponibles
