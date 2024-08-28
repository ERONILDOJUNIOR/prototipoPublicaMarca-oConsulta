import os
import re
from bs4 import BeautifulSoup

def mapear_arquivos(diretorio):
    html_files = []
    css_files = []
    js_files = []

    for root, _, files in os.walk(diretorio):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
            elif file.endswith('.css'):
                css_files.append(os.path.join(root, file))
            elif file.endswith('.js'):
                js_files.append(os.path.join(root, file))

    return html_files, css_files, js_files

def coletar_ids_classes_elementos(html_files):
    ids = set()
    classes = set()
    elements = set()

    for file in html_files:
        with open(file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            for tag in soup.find_all(True):
                elements.add(tag.name)
                if tag.has_attr('id'):
                    ids.add(tag['id'])
                if tag.has_attr('class'):
                    classes.update(tag['class'])

    return ids, classes, elements

def limpar_css(css_files, ids, classes, elements):
    for file in css_files:
        with open(file, 'r', encoding='utf-8') as f:
            css_content = f.read()

        # Remover seletores de classes, IDs e elementos não usados
        used_css = []
        for block in re.findall(r'[^{}]+\{[^}]+\}', css_content):
            selector = block.split('{')[0].strip()
            selectors = selector.split(',')
            keep_selector = False
            for sel in selectors:
                sel = sel.strip()
                if sel.startswith('.'):
                    if sel[1:] in classes:
                        keep_selector = True
                elif sel.startswith('#'):
                    if sel[1:] in ids:
                        keep_selector = True
                elif sel in elements:
                    keep_selector = True
            if keep_selector:
                used_css.append(block)

        # Escrever o CSS limpo de volta no arquivo
        with open(file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(used_css))

def encontrar_js_utilizados(html_files, js_files):
    used_js = set()
    js_dependencies = {}

    # Mapeia quais arquivos JS dependem de outros arquivos JS
    for file in js_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            js_dependencies[file] = re.findall(r'src\s*=\s*["\'](.+\.js)["\']', content)

    def mark_js_as_used(js_file):
        if js_file not in used_js:
            used_js.add(js_file)
            for dep in js_dependencies.get(js_file, []):
                dep_path = os.path.join(os.path.dirname(js_file), dep)
                if os.path.exists(dep_path):
                    mark_js_as_used(dep_path)

    # Encontra os arquivos JS que estão sendo referenciados nos HTMLs
    for file in html_files:
        with open(file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            for script in soup.find_all('script', src=True):
                js_file = os.path.join(os.path.dirname(file), script['src'])
                if os.path.exists(js_file):
                    mark_js_as_used(js_file)

    return used_js

def limpar_js(js_files, used_js):
    for file in js_files:
        if file not in used_js:
            os.remove(file)
            print(f"Arquivo JS removido: {file}")

def main(diretorio):
    html_files, css_files, js_files = mapear_arquivos(diretorio)
    ids, classes, elements = coletar_ids_classes_elementos(html_files)
    limpar_css(css_files, ids, classes, elements)
    used_js = encontrar_js_utilizados(html_files, js_files)
    limpar_js(js_files, used_js)
    print("Processo de limpeza concluído.")

# Substitua 'caminho/do/diretorio' pelo caminho real do diretório
if __name__ == "__main__":
    diretorio = 'caminho/do/diretorio'
    main(diretorio)
