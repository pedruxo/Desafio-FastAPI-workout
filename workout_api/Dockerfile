# Use a imagem oficial do Python como base, alterando para a versão 3.13.4
FROM python:3.13.4-slim

# Defina o diretório de trabalho no container
WORKDIR /app

# Copie o arquivo de dependências (requirements.txt) para o container e instale-as
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copie todo o código da sua aplicação para o diretório de trabalho
COPY ./ /app

# Exponha a porta que a aplicação irá rodar
EXPOSE 8000

# Comando para iniciar a aplicação com Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]