import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# response = requests.get('https://www.airbnb.com.br/')
# # print(response.text)

lista_de_hospedagens = []

flag  = None
while flag is None:
#instaciar
    opcoes = Options()
    # opcoes.add_argument('--headless') #roda o codigo sem abrir o navegador
    opcoes.add_argument('window-size=500,900')
    navegador = webdriver.Chrome(options=opcoes)
    navegador.get('https://www.airbnb.com.br/')
    print('resposta',navegador)
    
    time.sleep(2)

    # #definir tamanho da tela do chorme
    # print(site.prettify())
    try:
        # Aguarde o botão de cookies aparecer e clique nele
        WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="react-application"]/div/div/div[1]/div/div[4]/section/div/div[2]/div[1]/button'))  # Substitua o XPATH pelo seletor correto
        ).click()
        print("Botão de cookies clicado.")
    except Exception as e:
        print("Botão de cookies não encontrado ou erro:", e)
    time.sleep(1)
    campo_pesquisa_clicar =  navegador.find_element(By.XPATH,'//*[@id="react-application"]/div/div/div[1]/div/div[3]/div/div/div[2]/div/div[2]/div/div[1]/div/div/div/div[1]/button')
    campo_pesquisa_clicar.click()
    time.sleep(2)
    qual_cidade_procurar =  'Cabo Frio'
    
    digitar_pesquisa = campo_pesquisa_clicar.find_element(By.XPATH,'//*[@id="/homes-where-input"]')
    digitar_pesquisa.send_keys(qual_cidade_procurar)
    digitar_pesquisa.submit()


    #vai clicar no xpath da pagina atual
    #caso eu queira clicar em um ultimo botao da pagina eu boto [-1]
    pular_botao = campo_pesquisa_clicar.find_element(By.XPATH,'//*[@id="accordion-body-/homes-when"]/section/div/div/footer/button[1]')
    pular_botao.click()
    time.sleep(0.5)
    botao_buscar = campo_pesquisa_clicar.find_element(By.XPATH,'//*[@id="vertical-tabs"]/div[3]/footer/button[2]')
    botao_buscar.click()
    time.sleep(1)

    #chegando nas listas de casa vou converter o conteudo em beuatifulsoup
    
    #pagesource pega tipo um print do html onde a pagina está carrega
    

    time.sleep(5)    
    
    for i in range(5):  # Número de vezes que deseja rolar
        navegador.execute_script("window.scrollBy(0, 1800);")  # Rola 1000 pixels para baixo
        time.sleep(1) 
        
    print('procurando hospedagens...')   
    conteudo_da_pagina = navegador.page_source
    site = BeautifulSoup(conteudo_da_pagina, 'html.parser')
    

    #sempre em sequencia div dentro de div basicamente
    hospedagens = site.findAll('div',attrs={'itemprop':'itemListElement'})
    for hospedagem in hospedagens:
        descricao = hospedagem.find('meta',attrs={'itemprop':'name'})
        url_hospedagem = hospedagem.find('meta',attrs={'itemprop':'url'})
        procurar_preco = hospedagem.find('div',attrs={'class':'_i5duul'}) #.findAll('span')
        preco_achado = procurar_preco.find('span',attrs={'class':'_11jcbg2'})
        local_hospedagem = hospedagem.find('div',attrs={'class':'t1jojoys atm_g3_1kw7nm4 atm_ks_15vqwwr atm_sq_1l2sidv atm_9s_cj1kg8 atm_6w_1e54zos atm_fy_1vgr820 atm_7l_jt7fhx atm_cs_10d11i2 atm_w4_1eetg7c atm_ks_zryt35__1rgatj2 dir dir-ltr'})

    # print(hospedagem.prettify())


    #itemprop é o atributo geral das informacoes das hospedagens
     
        print('Hoteis:')
        obter_descricao = descricao['content']
        obter_url_hospedagem = url_hospedagem['content']
        obter_preco = preco_achado.text
        obter_lugar_hospedagem = local_hospedagem.text
        print(obter_descricao)
        print(obter_preco)
        print(obter_lugar_hospedagem)
        print()
        print('Link da hospedagem:',obter_url_hospedagem)
        # se eu quiser so o conteudo (texto) coloco na frente uma chave de 
        # dicionario  -- 
        print()
        
        lista_de_hospedagens.append([obter_descricao,obter_preco,obter_lugar_hospedagem,obter_url_hospedagem])


    print(lista_de_hospedagens)    
        
        



        
     
    dados_coletados= pd.DataFrame(lista_de_hospedagens,columns=['Hospedagem','Preço','Lugar','Link'])
    print(dados_coletados)
    
    def organiza_preco_asc(dados):
       tabela_asc = dados.sort_values(by='Preço',ascending=True)
       
       def cria_tabela(tabela):
           table_dados =tabela.to_excel('Tabela_hospedagens_asc.xlsx',index=False)
           return table_dados
       
       cria_tabela(tabela_asc)
       
       return tabela_asc
        
    organiza_preco_asc(dados_coletados) 
    
    continuar_sair = input('deseja [S]air ou [C]ontinuar')
    if continuar_sair.lower().startswith('s'):
        print('Até a proxima')
        break
    
    else:
        print('até a próxima')
        continue
    #fazer interface grafica