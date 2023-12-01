# # from .views_acc import *

import datetime
from bs4 import BeautifulSoup

context_main = {}


MIRROR_SOURCES = ["GET", "Cloudflare", "IPFS.io", "Infura"]
MIRROR_SOURCE_GET = ["GET"]



'''
def download_links_multi():
    try:
        links_to_download = []
        search_libgen_my = LibgenSearch_my()
        # if request.method == "POST":
        #     if request.POST.get('title_download_search', False):

        # results = s.search_title("Harry Potter i zakon feniksa")
        # print('results', results)

        results_my = search_libgen_my.search_title(title_download)

        if results_my:
            items_to_download_my = results_my
            print("items_to_download =", items_to_download_my)


        elif len(pdf_links) == 0:


                # items_to_download = results
                multi_links = [search_libgen.resolve_download_links(item_to_download) for item_to_download in items_to_download] 

                if len(else_links) > 0:
                    print("else_links", else_links)
                    context["pdf_links"] = else_links
                    context["len_pdf_links"] = len(else_links)
            
                    # else_links_id = [[else_links.index(else_link), else_link] for else_link in else_links]
                    # context["else_links_id"] = else_links_id
                    extentions = [val['Ext.'] for val in items_to_download]
                    if len(else_links) >= 2:

                        download_links_else_1a = else_links[0]["GET"].replace("get.php", "https://libgen.pm/get.php")
                        print("download_links_else_1a =", download_links_else_1a)
                        context["download_links_1a"] = download_links_else_1a
                        context["extention_1a"] = extentions[0]

                        download_links_else_2a = else_links[1]["GET"].replace("get.php", "https://libgen.pm/get.php")
                        context["download_links_2a"] = download_links_else_2a
                        context["extention_2a"] = extentions[1]
                        
                        print("else download_links_2a =", download_links_else_2a)
                        context["message_read_download_not_pdf"] = "This book is probably not available for download in pdf, press buttons below to download in differt format."
                        return Response(context, template_name='download_book.html',)

                    elif len(else_links) == 1:
                        download_links_else_1a = else_links[0]["GET"].replace("get.php", "https://libgen.pm/get.php")
                        context["download_links_1a"] = download_links_else_1a
                        context["extention_1a"] = extentions[0]
                        print("download_links_else_1a =", download_links_else_1a)
                        context["message_read_download_not_pdf"] = "This book is probably not available for download in pdf, press button below to download in other format."
                        return Response(context, template_name='download_book.html',)

                    elif len(else_links) == 0:
                        context["message_read_download"] = "This book is probably not available for download, below is the last chance for those who persevere"
                        # print("2. title_download", title_download)
                        # title_slugify = slugify(title_download).replace(" ", "+").replace(" ", "-")
                        return Response(context, template_name='download_book.html',)

    except Exception as e:
        print(f'Exception as e else_links, reason: {e}')
        context["message_read_download"] = "This book is probably not available for download"
        # print("3. title_download", title_download)
        return Response(context, template_name='download_book.html',)


    context["search_title_download"] = BookDownload()
    return Response(context, template_name='download_book.html', ) '''