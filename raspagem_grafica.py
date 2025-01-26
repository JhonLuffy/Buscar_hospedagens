import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import flet as ft
import os

# Função para coletar as hospedagens
def coleta_hospedagens(cidade, page):
    lista_de_hospedagens = []
    
    # Instanciar navegador
    opcoes = Options()
    opcoes.add_argument('window-size=400,800')
    navegador = webdriver.Chrome(options=opcoes)
    navegador.get('https://www.airbnb.com.br/')
    
    time.sleep(2)

    try:
        # Clique no botão de cookies
        WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="react-application"]/div/div/div[1]/div/div[4]/section/div/div[2]/div[1]/button'))
        ).click()
    except Exception as e:
        print("Botão de cookies não encontrado ou erro:", e)
    time.sleep(1)
    
    campo_pesquisa_clicar = navegador.find_element(By.XPATH, '//*[@id="react-application"]/div/div/div[1]/div/div[3]/div/div/div[2]/div/div[2]/div/div[1]/div/div/div/div[1]/button')
    campo_pesquisa_clicar.click()
    time.sleep(2)
    
    digitar_pesquisa = campo_pesquisa_clicar.find_element(By.XPATH, '//*[@id="/homes-where-input"]')
    digitar_pesquisa.send_keys(cidade)
    digitar_pesquisa.submit()
    pular_botao = campo_pesquisa_clicar.find_element(By.XPATH, '//*[@id="accordion-body-/homes-when"]/section/div/div/footer/button[1]')
    pular_botao.click()
    time.sleep(0.5)
    botao_buscar = campo_pesquisa_clicar.find_element(By.XPATH, '//*[@id="vertical-tabs"]/div[3]/footer/button[2]')
    botao_buscar.click()
    time.sleep(1)
    page.add(ft.Text("Buscando hospedagens...", size=18, color=ft.Colors.WHITE))
    # Rolando a página de maneira controlada
    for _ in range(3):  # Alterar número de rolagens conforme necessário
        navegador.execute_script("window.scrollBy(0, 1800);")
        time.sleep(1)
    
    
    
    conteudo_da_pagina = navegador.page_source
    site = BeautifulSoup(conteudo_da_pagina, 'html.parser')
    
    hospedagens = site.findAll('div', attrs={'itemprop': 'itemListElement'})
    
    for hospedagem in hospedagens:
        descricao = hospedagem.find('meta', attrs={'itemprop': 'name'})
        url_hospedagem = hospedagem.find('meta', attrs={'itemprop': 'url'})
        procurar_preco = hospedagem.find('div', attrs={'class': '_i5duul'})
        preco_achado = procurar_preco.find('span', attrs={'class': '_11jcbg2'})
        local_hospedagem = hospedagem.find('div', attrs={'class': 't1jojoys atm_g3_1kw7nm4 atm_ks_15vqwwr atm_sq_1l2sidv atm_9s_cj1kg8 atm_6w_1e54zos atm_fy_1vgr820 atm_7l_jt7fhx atm_cs_10d11i2 atm_w4_1eetg7c atm_ks_zryt35__1rgatj2 dir dir-ltr'})
        
        obter_descricao = descricao['content']
        obter_url_hospedagem = url_hospedagem['content']
        obter_preco = preco_achado.text
        obter_lugar_hospedagem = local_hospedagem.text

        lista_de_hospedagens.append([obter_descricao, obter_preco, obter_lugar_hospedagem, obter_url_hospedagem])
    
    # Criando o DataFrame com as hospedagens coletadas
    dados_coletados = pd.DataFrame(lista_de_hospedagens, columns=['Hospedagem', 'Preço', 'Lugar', 'Link'])
    
    # Exibindo o DataFrame no Flet com rolagem
    page.add(ft.Text(f"Hospedagens encontradas em {cidade}:", size=20, color=ft.Colors.WHITE))
    
    data_table = ft.DataTable(columns=[ft.DataColumn(ft.Text(col)) for col in dados_coletados.columns], rows=[ 
        ft.DataRow(cells=[ft.DataCell(ft.Text(str(cell))) for cell in row]) for row in dados_coletados.values.tolist()
    ])
    
    page.add(ft.Column([data_table], scroll=True, expand=True))
    
    # Criando o arquivo Excel
    dados_coletados.to_excel('Tabela_hospedagens_asc.xlsx', index=False)
    
    return dados_coletados

# Função principal para o Flet
def main(page: ft.Page):
    page.add(ft.Text("Consulte as hospedagens de onde você quer", size=20, color=ft.Colors.WHITE))
    page.add(ft.Text("Digite a cidade:", size=16, color=ft.Colors.WHITE))
    
    cidade_input = ft.TextField(label="Cidade", autofocus=True)
    page.add(cidade_input)
    
    # Função de busca de hospedagens
    def on_search_click(e):
        cidade = cidade_input.value
        if cidade:
            coleta_hospedagens(cidade, page)
        else:
            page.add(ft.Text("Digite uma cidade válida.", color=ft.Colors.RED))

    # Botão de busca
    search_button = ft.ElevatedButton("Buscar", on_click=on_search_click)
    page.add(search_button)
    
    # Função para simular o download do arquivo Excel
    def on_download_click(e):
        page.add(ft.Text("Baixando o arquivo..."))
        # Simula o download
        time.sleep(1)
        page.add(ft.Text("Arquivo Tabela_hospedagens_asc.xlsx pronto para download!"))
        
        # Exibe o link para download
        download_link = ft.ElevatedButton(
            text="Clique para baixar o arquivo",
            on_click=lambda e: page.launch_url('file:///' + os.path.abspath('Tabela_hospedagens_asc.xlsx'))
        )
        page.add(download_link)

    # Botão para baixar o arquivo Excel
    download_button = ft.ElevatedButton("Ver Tabela", on_click=on_download_click)
    page.add(download_button)

# Executando o aplicativo Flet
ft.app(target=main)
