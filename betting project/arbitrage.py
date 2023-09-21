import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from fuzzywuzzy import process, fuzz
import pandas as pd




#day = "today"
day = "tomorrow"


def is_arbitrage_3(odds):
    """
    Calculates the sum of the implied probability for a set of football odds with all outcomes (win, draw or loss). 
    If the odds don't have a suitable format (a list with three numbers) it returns 1.

    Args:
        odds (list): list of the odds

    Returns:
        float: the sum of the implied probability
    """
    try:
        odds = [float(odds[0].replace(",",".")),float(odds[1].replace(",",".")),float(odds[2].replace(",","."))]
        return (1/odds[0]) + (1/odds[1]) + (1/odds[2])
    except:
        return 1

def send_mail(message):
    """Sends an email with a message

    Args:
        message (string): message to be send
    """
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import smtplib
 
    # create message object instance
    msg = MIMEMultipart()
 
    # setup the parameters of the message
    password = "ranukkuciltmeqvw"
    msg['From'] = "js3195297@gmail.com"
    msg['To'] = "js3195297@gmail.com"
    msg['Subject'] = "arbitrage oportunity"
 
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
 
    #create server
    server = smtplib.SMTP('smtp.gmail.com: 587')
 
    server.starttls()
 
    # Login Credentials for sending the mail
    server.login(msg['From'], password)
 
 
    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())
 
    server.quit()

def display_results(frame, name1,name2):
    """
    Creates the message to be send by email with the game and the odds. 
    Args:
        frame (Pandas.Dataframe): a DataFrame with the different combination of odds from the different bookmakers 
        name1 (string): name of the home team
        name2 (string): name of the other team
    """

    for i in range(len(frame)):
            name_columns = ['sure_bet1','sure_bet2','sure_bet3','sure_bet4','sure_bet5','sure_bet6','sure_bet7','sure_bet8']
            sure_bets_list = [(frame.iloc[i,j+4],name_columns[j]) for j in range(len(name_columns)) if frame.iloc[i,j+4] < 1]
            message = f'{frame.iloc[i,0]}, {name1}, {frame.iloc[i,2]}, {name2}: '
            for j in range(len(sure_bets_list)):
                if sure_bets_list[j][1] == 'sure_bet1':
                    message_final = message + f'casa - {frame.iloc[i,1][0]}, {name1}; empate - {frame.iloc[i,1][1]}, {name1}, fora - {frame.iloc[i,1][2]}, {name1}'
                    send_mail(message_final)
                elif sure_bets_list[j][1] == 'sure_bet2':
                    message_final = message + f'casa - {frame.iloc[i,3][0]}, {name2}; empate - {frame.iloc[i,3][1]}, {name2}, fora - {frame.iloc[i,3][2]}, {name2}'
                    send_mail(message_final)
                elif sure_bets_list[j][1] == 'sure_bet3':
                    message_final = message + f'casa - {frame.iloc[i,1][0]}, {name1}; empate - {frame.iloc[i,1][1]}, {name1}, fora - {frame.iloc[i,3][2]}, {name2}'
                    send_mail(message_final)
                elif sure_bets_list[j][1] == 'sure_bet4':
                    message_final = message + f'casa - {frame.iloc[i,1][0]}, {name1}; empate - {frame.iloc[i,3][1]}, {name2}, fora - {frame.iloc[i,3][2]}, {name2}'
                    send_mail(message_final)
                elif sure_bets_list[j][1] == 'sure_bet5':
                    message_final = message + f'casa - {frame.iloc[i,3][0]}, {name2}; empate - {frame.iloc[i,1][1]}, {name1}, fora - {frame.iloc[i,1][2]}, {name1}'
                    send_mail(message_final)
                elif sure_bets_list[j][1] == 'sure_bet6':
                    message_final = message + f'casa - {frame.iloc[i,3][0]}, {name2}; empate - {frame.iloc[i,3][1]}, {name2}, fora - {frame.iloc[i,1][2]}, {name1}'
                    send_mail(message_final)
                elif sure_bets_list[j][1] == 'sure_bet7':
                    message_final = message + f'casa - {frame.iloc[i,1][0]}, {name1}; empate - {frame.iloc[i,3][1]}, {name2}, fora - {frame.iloc[i,1][2]}, {name1}'
                    send_mail(message_final)
                elif sure_bets_list[j][1] == 'sure_bet8':
                    message_final = message + f'casa - {frame.iloc[i,3][0]}, {name2}; empate - {frame.iloc[i,1][1]}, {name1}, fora - {frame.iloc[i,3][2]}, {name2}'
                    send_mail(message_final)

def find_surebet(frame):
    """takes a dataFrame with the odds of two bookmakers and test different combinations of odds and return a DataFrame with the combination of odds that has a sum of implicit probabilities less than 1 (arbitrage opportunitie)

    Args:
        frame (Pandas.DataFrame): dataFrame with the odds of two bookmakers

    Returns:
        Pandas.DataFrame: dataframe with the different combinations of odds that represent a arbitrage opportunity
    """
    frame[['odds_x1','odds_x2','odds_x3']] = frame['odds_x'].apply(pd.Series).astype(float)    
    frame[['odds_y1','odds_y2','odds_y3']] = frame['odds_y'].apply(pd.Series).astype(float)
    frame['sure_bet1'] = (1/frame['odds_x1']) + (1/frame['odds_x2']) + (1/frame['odds_x3'])
    frame['sure_bet2'] = 1/frame['odds_y1'] + 1/frame['odds_y2'] + 1/frame['odds_y3']
    frame['sure_bet3'] = 1/frame['odds_x1'] + 1/frame['odds_x2'] + 1/frame['odds_y3']
    frame['sure_bet4'] = 1/frame['odds_x1'] + 1/frame['odds_y2'] + 1/frame['odds_y3']
    frame['sure_bet5'] = 1/frame['odds_y1'] + 1/frame['odds_x2'] + 1/frame['odds_x3']
    frame['sure_bet6'] = 1/frame['odds_y1'] + 1/frame['odds_y2'] + 1/frame['odds_x3']
    frame['sure_bet7'] = 1/frame['odds_x1'] + 1/frame['odds_y2'] + 1/frame['odds_x3']
    frame['sure_bet8'] = 1/frame['odds_y1'] + 1/frame['odds_x2'] + 1/frame['odds_y3']
    frame = frame[(frame['sure_bet1'] < 1) | (frame['sure_bet2'] < 1) | (frame['sure_bet3'] < 1) | (frame['sure_bet4'] < 1) | (frame['sure_bet5'] < 1) | (frame['sure_bet6'] < 1) | (frame['sure_bet7'] < 1) | (frame['sure_bet8'] < 1)]
    frame = frame[['teams_x','odds_x','teams_y','odds_y', 'sure_bet1','sure_bet2','sure_bet3','sure_bet4','sure_bet5','sure_bet6','sure_bet7','sure_bet8']]
    frame.reset_index(drop=True,inplace=True)
    return frame




for i in range (20):
    betclic = []
    #betclic
    web = 'https://www.betclic.pt/futebol-s1'
    os.environ["PATH"] += r"C:/Users/lmir/OneDrive/Ambiente de Trabalho/betting"


    driver = webdriver.Chrome()
    driver.get(web)
    dates = driver.find_elements(By.CLASS_NAME, "groupEvents_content")
    while len(dates) < 4:
        game = driver.find_elements(By.TAG_NAME, "sports-events-event")[-1]
        actions = ActionChains(driver)
        actions.move_to_element(game).perform()
        time.sleep(5)
        dates = driver.find_elements(By.CLASS_NAME, "groupEvents_content")

    #get the list of games for a day or for the next day
    if day == "tomorrow":
        games = dates[2].find_elements(By.TAG_NAME, "sports-events-event")
    else:
        games = dates[1].find_elements(By.TAG_NAME, "sports-events-event")

    for game in games:
        actions = ActionChains(driver)
        actions.move_to_element(game).perform()
        #save the name of the teams and odds for each game
        try:
            names = [game.find_elements(By.CLASS_NAME, "scoreboard_contestantLabel")[0].text, game.find_elements(By.CLASS_NAME, "scoreboard_contestantLabel")[1].text]
            odds = [game.find_elements(By.CLASS_NAME, "oddValue")[0].text, game.find_elements(By.CLASS_NAME, "oddValue")[1].text, game.find_elements(By.CLASS_NAME, "oddValue")[2].text]
            betclic.append([names, odds])
        except:
            continue
    driver.quit()

    for game in betclic:
        #try to find arbitrage oportunities at Betclic odds
        if is_arbitrage_3(game[1]) < 1:
            message = f'{game[0][0]} vs {game[0][1]}, {game[1]}, betclic'
            send_mail(message)

    #bwin
    bwin = []

    if day == "tomorrow":
        web = "https://sports.bwin.pt/pt/sports/futebol-4/amanh%C3%A3"
    else:
        web = 'https://sports.bwin.pt/pt/sports/futebol-4/hoje'

    os.environ["PATH"] += r"C:/Users/lmir/OneDrive/Ambiente de Trabalho/betting"


    driver = webdriver.Chrome()
    driver.get(web)

    WebDriverWait(driver, 30).until( 
            EC.presence_of_all_elements_located(
                (By.ID, 'onetrust-accept-btn-handler')
            )
        )

    driver.find_element(By.ID, "onetrust-accept-btn-handler").click()

    for i in range(10):
            driver.execute_script("window.scrollTo(0,0)") 
            footer = driver.find_element(By.CLASS_NAME, "footer-wrapper")
            actions = ActionChains(driver)
            actions.move_to_element(footer).perform()
            time.sleep(3)


    driver.execute_script("window.scrollTo(0,0)") 

    WebDriverWait(driver, 30).until( 
            EC.presence_of_all_elements_located(
                (By.TAG_NAME, 'ms-event')
            )
        )

    games = driver.find_elements(By.TAG_NAME, "ms-event")

    for game in games:
            actions = ActionChains(driver)
            actions.move_to_element(game).perform()
            #save the name of the teams and odds for each game
            try:
                names = [game.find_elements(By.CLASS_NAME, "participant")[0].text, game.find_elements(By.CLASS_NAME, "participant")[1].text]
                odds = game.find_elements(By.TAG_NAME, "ms-option-group")[0]
                odds_list = [odds.find_elements(By.TAG_NAME, "ms-font-resizer")[0].text, odds.find_elements(By.TAG_NAME, "ms-font-resizer")[1].text, odds.find_elements(By.TAG_NAME, "ms-font-resizer")[2].text]
                bwin.append([names, odds_list])
            except:
                continue
            
    driver.quit()

    for game in bwin:
       #try to find arbitrage oportunities at Bwin odds
        if is_arbitrage_3(game[1]) < 1:
            message =  f'{game[0][0]} vs {game[0][1]}, {game[1]}, bwin'
            send_mail(message)

        #betano
    betano = []
    web = 'https://www.betano.pt/sport/futebol/jogos-de-hoje/?sort=Leagues'
    os.environ["PATH"] += r"C:/Users/lmir/OneDrive/Ambiente de Trabalho/betting" 

    driver = webdriver.Chrome()
    driver.get(web)

    try:

        driver.find_element(By.CLASS_NAME, "sb-modal__close__btn").click()
    except:
        pass

    try:
        driver.find_element(By.CLASS_NAME, "sticky-notification__cta--secondary").click()
    except:
        pass
    leagues = driver.find_elements(By.CLASS_NAME, "league-block")

    for league in leagues:
        #save the name of the teams and odds for each game
        try:
            if league.find_element(By.CSS_SELECTOR, "svg:nth-child(2)").get_attribute("class") != "sb-arrow kz-icon-xs sb-arrow--collapsed push-right icon--clickable":
                league.find_element(By.CSS_SELECTOR, "svg:nth-child(2)").click()
            games = league.find_elements(By.CLASS_NAME, "events-list__grid__event")
            for game in games:
                name = [game.find_elements(By.CLASS_NAME, "events-list__grid__info__main__participants__participant-name")[0].text, game.find_elements(By.CLASS_NAME, "events-list__grid__info__main__participants__participant-name")[1].text]
                odds = [game.find_elements(By.CLASS_NAME, "selections__selection__odd")[0].text, game.find_elements(By.CLASS_NAME, "selections__selection__odd")[1].text, game.find_elements(By.CLASS_NAME, "selections__selection__odd")[2].text]
                betano.append([name, odds])
        except:
            continue
    driver.quit()

    for game in betano:
         #try to find arbitrage oportunities at Betano odds
        if is_arbitrage_3(game[1]) < 1:
            message = f'{game[0][0]} vs {game[0][1]}, {game[1]}, betano'
            send_mail(message)


    #
    teams_bwin = [f'{game[0][0]} {game[0][1]}' for game in bwin if (game[0][0] != "" and game[0][1] != "") and (game[1][0] != "" and game[1][1] != "" and game[1][2] != "")]
    teams_betclic = [f'{game[0][0]} {game[0][1]}' for game in betclic]
    teams_betano = [f'{game[0][0]} {game[0][1]}' for game in betano]

    odds_bwin = [[game[1][0].replace(",","."),game[1][1].replace(",","."),game[1][2].replace(",",".")] for game in bwin if (game[0][0] != "" and game[0][1] != "") and (game[1][0] != "" and game[1][1] != "" and game[1][2] != "")]
    odds_betclic = [[game[1][0].replace(",","."),game[1][1].replace(",","."),game[1][2].replace(",",".")] for game in betclic]
    odds_betano = [[game[1][0].replace(",","."),game[1][1].replace(",","."),game[1][2].replace(",",".")] for game in betano]

    games_bwin = pd.DataFrame.from_dict({"teams":teams_bwin, "odds":odds_bwin})
    games_betclic = pd.DataFrame.from_dict({"teams":teams_betclic, "odds":odds_betclic})
    games_betano = pd.DataFrame.from_dict({"teams":teams_betano, "odds":odds_betano})




    teams_1 = teams_bwin
    teams_2 = teams_betclic
    teams_3 = teams_betano


    #games_betano[['Teams_matched_betano_betclic', 'Score_betano_betclic']] = games_betano['teams'].apply(lambda x:process.extractOne(x, teams_2, scorer=fuzz.partial_ratio)).apply(pd.Series)
    #games_bwin[['Teams_matched_bwin_betclic', 'Score_bwin_betclic']] = games_bwin['teams'].apply(lambda x:process.extractOne(x, teams_2, scorer=fuzz.partial_ratio)).apply(pd.Series)
    #games_bwin[['Teams_matched_bwin_betano', 'Score_bwin_betano']] = games_bwin['teams'].apply(lambda x:process.extractOne(x, teams_3, scorer=fuzz.partial_ratio)).apply(pd.Series)
    


    df_bwin_betclic = pd.merge(games_bwin, games_betclic, left_on='Teams_matched_bwin_betclic', right_on='teams')
    df_bwin_betano = pd.merge(games_bwin, games_betano, left_on='Teams_matched_bwin_betano', right_on='teams')
    df_betano_betclic = pd.merge(games_betano, games_betclic, left_on='Teams_matched_betano_betclic', right_on='teams')

    df_bwin_betclic = df_bwin_betclic[df_bwin_betclic['Score_bwin_betclic']>70]
    df_bwin_betclic = df_bwin_betclic[['teams_x', 'odds_x', 'teams_y', 'odds_y']]

    df_bwin_betano = df_bwin_betano[df_bwin_betano['Score_bwin_betano']>70]
    df_bwin_betano = df_bwin_betano[['teams_x', 'odds_x', 'teams_y', 'odds_y']]

    df_betano_betclic = df_betano_betclic[df_betano_betclic['Score_betano_betclic']>70]
    df_betano_betclic = df_betano_betclic[['teams_x', 'odds_x', 'teams_y', 'odds_y']]


    df_surebet_betano_betclic = find_surebet(df_betano_betclic)
    df_surebet_bwin_betano = find_surebet(df_bwin_betano)
    df_surebet_bwin_betclic = find_surebet(df_bwin_betclic)

    display_results(df_surebet_bwin_betclic,"bwin","betclic")
    display_results(df_surebet_bwin_betano,"bwin","betano")
    display_results(df_surebet_betano_betclic, "betano", "betclic")