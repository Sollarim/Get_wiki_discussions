import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString

BASE_WIKI_ADRESS = "https://fr.wikipedia.org/wiki/"


def get_wiki_discus_response():

    response = requests.get(BASE_WIKI_ADRESS + "Sp%C3%A9cial:Page_au_hasard", allow_redirects=True, timeout=10)
    url = response.url

    #print("Get random page %s"%url)

    page_name = url.split('/')[-1]

    discussion_url = BASE_WIKI_ADRESS + "Discussion:" + page_name

    response = requests.get(discussion_url)

    return response

def is_wiki_discus_parsed_page_empty(parsed_wiki_page):
    if parsed_wiki_page.body.find('div',attrs={'class':'noarticletext'}) != None:
        return True
    else:
        return False
    
def is_wiki_bandeau(tag):
    if ('class' in tag.attrs.keys()) and ("bandeau-container" in tag['class']):
        return True
    else:
        return False
    
def get_discussion_text(parsed_wiki_discuss):
    texte = ""
    content = parsed_wiki_discuss.body.find('div',attrs={'class':'mw-content-ltr'})
    for part in content.children:
        if not isinstance(part,NavigableString):
            if not is_wiki_bandeau(part):
                texte += part.text
    return texte
    

def main():

    n_ok_page = 0

    while (n_ok_page < 5):

        response = get_wiki_discus_response()
        print("Get random discussion page %s"%response.url)
        parsed_html = BeautifulSoup(response.content, "html.parser")

        if is_wiki_discus_parsed_page_empty(parsed_html):
            print("This Discussion page is empty :(")
        else:
            texte = get_discussion_text(parsed_html)
            if texte == "":
                print("This Discussion page is only bandeau")
            else:
                n_ok_page += 1
                filename = "pages/" + response.url.split("Discussion:")[-1] + ".txt"
                print(texte)
                with open(filename,'wb') as txt_file:
                    txt_file.write(texte.encode('utf-8'))

if __name__ == "__main__":
    main()