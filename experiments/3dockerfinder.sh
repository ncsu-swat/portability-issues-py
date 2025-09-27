#!/bin/bash

# Script para contar projetos únicos que usam Docker
# Procura por Dockerfile e arquivos docker-compose

echo "🐳 Analisando projetos com Docker..."
echo "======================================"

cd projects

# Procurar por arquivos Docker e coletar diretórios únicos
docker_projects=$(find . -maxdepth 2 \( \
    -name "Dockerfile" -o \
    -name "docker-compose.yml" -o \
    -name "docker-compose.yaml" -o \
    -name "compose.yml" -o \
    -name "compose.yaml" \
\) -exec dirname {} \; | sort | uniq)

# Contar projetos únicos
total_projects=$(echo "$docker_projects" | grep -v "^\.$" | wc -l)

# Verificar se encontrou projetos
if [[ $total_projects -eq 0 ]]; then
    echo "❌ Nenhum projeto com Docker foi encontrado."
    exit 0
fi

echo "📋 Projetos encontrados com Docker:"
echo ""

# Listar cada projeto e seus arquivos Docker
for project in $docker_projects; do
    if [[ "$project" != "." ]]; then
        project_name=$(basename "$project")
        docker_files=""
        
        # Verificar quais arquivos Docker existem
        if [[ -f "$project/Dockerfile" ]]; then
            docker_files="$docker_files Dockerfile"
        fi
        if [[ -f "$project/docker-compose.yml" ]]; then
            docker_files="$docker_files docker-compose.yml"
        fi
        if [[ -f "$project/docker-compose.yaml" ]]; then
            docker_files="$docker_files docker-compose.yaml"
        fi
        if [[ -f "$project/compose.yml" ]]; then
            docker_files="$docker_files compose.yml"
        fi
        if [[ -f "$project/compose.yaml" ]]; then
            docker_files="$docker_files compose.yaml"
        fi
        
        echo "  📂 $project_name →$docker_files"
    fi
done

echo ""
echo "======================================"
echo "🎯 Total de projetos únicos com Docker: $total_projects"
echo "======================================"

# Estatísticas adicionais
dockerfile_count=$(find . -maxdepth 2 -name "Dockerfile" | wc -l)
compose_count=$(find . -maxdepth 2 \( -name "docker-compose.yml" -o -name "docker-compose.yaml" -o -name "compose.yml" -o -name "compose.yaml" \) | wc -l)

echo ""
echo "📊 Estatísticas:"
echo "  • Projetos com Dockerfile: $dockerfile_count"
echo "  • Projetos com Compose: $compose_count"