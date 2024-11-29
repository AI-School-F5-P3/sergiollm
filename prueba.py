import torch
print(torch.__version__)  # Verifica que la versión de PyTorch sea la correcta
print(torch.cuda.is_available())  # Esto debería devolver True si CUDA está habilitado
print(torch.cuda.get_device_name(0))  # Deberías ver el nombre de tu GPU
