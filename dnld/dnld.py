import urllib.request

def dnld():
        sites = ["https://lenta.ru/articles/2016/04/20/put_k_uspekhu/", "https://lenta.ru/news/2016/04/21/omsk_mites/", "https://lenta.ru/news/2016/04/21/omsk_mites/"]

        count = 1
        for url in sites:
                with open('site{0}'.format(count), 'w', encoding = 'utf8') as s$
                        st = urllib.request.urlopen(url)
                        f = st.read()
                        site.write(str(f))
                        count += 1
dnld()