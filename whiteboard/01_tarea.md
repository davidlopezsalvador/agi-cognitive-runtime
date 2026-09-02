# Tarea: Test A/B del AGI Cognitive Runtime

## Objetivo
Ejecutar el test A/B comparando el runtime con y sin knowledge literario.

## Instrucciones
1. Clona el repo: git clone https://github.com/davidlopezsalvador/agi-cognitive-runtime.git
2. Instala dependencias: pip install -e ".[dev]"
3. Ejecuta el test: python -c "import sys; sys.path.insert(0, 'src'); from benchmarks.compare_literary_knowledge import run_comparison; run_comparison(None)"
4. Documenta los resultados en whiteboard/02_resultados.md

## Contexto
- El proyecto tiene 175 tests pasando
- Hay 2 entradas de conocimiento literario (Lazarillo + Quijote)
- El test necesita un LLM provider para ser significativo
- Sin provider, ambos modos dan la misma respuesta template

## Entregable
Archivo whiteboard/02_resultados.md con los resultados del test.
