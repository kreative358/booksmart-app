import os, re, json, time, requests, datetime
from django.utils.text import slugify
from rest_framework.response import Response

def use_title_author(context, formlib, book, identities_1, idents_title_1, idents_author_1, idents_1, titles_idents_1, identities):
    # identities_1a = []
    parameters = ""

    titles_split = []
    titles_short = []
    titles_split_q = []
    titles_short_q = []
    titles_plus = []
    titles_plus_q = []

    idents = []
    # idents.clear()

    idents_title = []
    # idents_title.clear()

    idents_author = []
    # idents_author.clear()

    titles_jsplit = []
    titles_jshort = []
    authors_jname = []
    authors_jsurname = []

    if formlib.is_valid():
        
        title_to_search = book.title
        title_to_search_split = title_to_search.lower().replace("the ", "").replace(":", "").split()
        auth_to_search = book.author
        author_to_search = auth_to_search.lower()
        auth_surname = book.surname
        author_surname = auth_surname.lower()
        print('title_to_search', title_to_search)

        title_to_search_q = title_to_search.lower().replace("the ", "").replace("-", "slugify")
        title_slugify_q = slugify(title_to_search_q).replace("-", " ").replace("slugify", "-")
        title_split_q = title_slugify_q.split()
        author_to_search_q = author_to_search.replace("-", "slugify")
        author_slugify_q = slugify(author_to_search_q).replace("-", " ").replace("slugify", "-")
        author_split_q = author_slugify_q.split()
        auth_surname_q = author_surname.replace("-", "slugify")
        author_surname_slugify_q = slugify(auth_surname_q).replace("-", " ").replace("slugify", "-")
        author_surname_q = author_surname_slugify_q

        if len(title_to_search_split) > 5:
            title_split_short = title_to_search_split[:5]
            titles_split.append(title_split_short)
            title_split_short_q = title_split_q[:5]
            titles_split_q.append(title_split_short_q)
            title_short = " ".join(title_split_short)
            titles_short.append(title_short)
            title_short_q = " ".join(title_split_short_q)
            #title_ident = "".join(title_split_short_q)
            titles_idents_1.append("".join(title_split_short_q))
            title_plus = title_short.replace(' ', '+')
            titles_plus.append(title_plus)
            title_plus_q = title_short_q.replace(' ', '+')
            titles_plus_q.append(title_plus)
            print('if title_plus', title_plus)
        else:
            title_split_short = title_to_search_split
            titles_split.append(title_split_short)
            title_short = " ".join(title_split_short)
            titles_short.append(title_short)
            title_plus = title_short.replace(' ', '+')
            titles_plus.append(title_plus)
            print('else title_plus', title_plus)
            title_split_short_q = title_split_q
            titles_split.append(title_split_short_q)
            titles_idents_1.append("".join(title_split_short_q))
            title_short_q = " ".join(title_split_short_q)
            titles_short_q.append(title_short_q)
            title_plus_q = title_slugify_q.replace(' ', '+')
            titles_plus_q.append(title_plus_q)

        # parameters = f'{title_plus}+{author_surname}'
        parameters = f'{title_plus_q}+{author_surname_q}'
        print('parameters:', parameters)
        search_url = f'https://openlibrary.org/search/inside.json?q={parameters}'
        print('search_url', search_url)
        # search_url = f'https://openlibrary.org/search/inside.json?q={title_plus}'
        r = requests.get(url=search_url)
        if r.status_code != 200:
            context['message_read'] = f'Sorry, probably something went wrong, r.status_code = {r.status_code}'
            return Response(context, template_name='read_book.html', )

        data = r.json()
        # data = r
        # records = json.loads(data)
        records = data
        links = []

        # url = 'https://openlibrary.org/account/login'
        # context['searching'] = url

        # url = 'https://archive.org/account/login'
        # url = 'https://openlibrary.org/account/login'
        # searching = f'{url}'
        
        # idents = []
        # idents_title = []
        # idents_author = []
        # titles_jsplit = []
        # titles_jshort = []
        # authors_jname = []
        # authors_jsurname = []
        
        if records['hits']['hits']:
            recs = records['hits']['hits']
            print('len(recs)', len(recs))
            n_records = len(recs)
            print('titles_short[-1]', titles_short[-1])
            # for i in range(n_records-1):
            for i in range(n_records):
                try:
                    if recs[i]['edition']['ocaid']:
                        ident = recs[i]['edition']['ocaid']
                        idents.append(ident)
                except Exception as e:
                    print(f"151 {e}, i: {i}")
                    
                try:
                    if recs[i]['edition']['title']:
                        title_jshort = recs[i]['edition']['title'].lower()
                        # print('title_jshort', title_jshort)
                        # print('titles_short[0]', titles_short[0])
                        titles_jshort.append(title_jshort)
                        title_jsplit = title_jshort.split()
                        titles_jsplit.append(title_jsplit)

                        if title_jshort==title_short or set(title_jsplit).issubset(set(title_split_short)) or set(title_split_short).issubset(set(title_jsplit)):
                            idents_title.append(idents[-1])
                        # if title_jshort==titles_short[0] set(title_jsplit).issubset(set(titles_split[0])) or set(titles_split[0]).issubset(set(title_jsplit)):
                        #     idents_title.append(idents[-1])

                        else:
                            print('1. no title')
                    else:
                        print('2. no title')
                except Exception as e:
                    print(f"168 {e}, i: {i}")
                try:
                    if recs[i]['edition']['authors'][0]['name']:
                        author_jname = recs[i]['edition']['authors'][0]['name'].lower()
                        authors_jname.append(author_jname)
                        author_jsurname = author_jname.split()[-1]
                        authors_jsurname.append(author_jsurname)
                        if author_jname == author_to_search or author_jsurname == author_surname:
                            idents_author.append(idents[-1])
                        else:
                            print('1. no author')
                            
                    else:
                        print('2. no author')
                        
                except Exception as e:
                    print(f"180 {e}, i: {i}")

            print('163 idents', idents)
            # print('idents_title', idents_title)
            # print('idents_author', idents_author)

            if idents and idents_title and idents_author:
                identities_list_1 = list(set(idents).intersection(set(idents_title).intersection(set(idents_author))))
                # identities.extend(identities_list_1)
                if len(identities_list_1) > 0:
                    identities_1.extend(identities_list_1)
                    print('identities_list_1', identities_list_1)
                    identities.extend(identities_list_1)
                    
                else:
                    print('1. no links')

            elif idents and idents_title and not idents_author:
                identities_list_2 = list(set(idents).intersection(set(idents_title)))
                # identities.extend(identities_list_2)
                if len(identities_list_2) > 0:
                    identities_1.extend(identities_list_2)
                    print('identities_list_2', identities_list_2)
                    identities.extend(identities_list_2)
                else:
                    print('2. no links')
                    idents_title_1.extend(idents_title)

            elif idents and idents_author and not idents_title:
                identities_list_3 = list(set(idents).intersection(set(idents_title)))
                # identities.extend(identities_list_3)
                if len(identities_list_3) > 0:
                    identities_1.extend(identities_list_3)
                    print('identities_list_3', identities_list_3)
                    identities.extend(identities_list_3)
                else:
                    print('19 3. no links')
                    idents_author_1.extend(idents_author)
                    idents_1.extend(idents)



            else:
                print('4 no links')
                pass
                #context['message'] = 'Sorry, probably no free ebook on this title'
                #return Response(context, template_name='read_book.html', )

        else:
            print('5 no links')

            #context['message'] = 'Sorry, probably there is no this book to read for free'
            #return Response(context, template_name='read_book.html', )    
        # return identities



def include_ident_1(idents_1, titles_idents_1, container, context, titles_idents_2):

    t_ident = titles_idents_1[-1]
    titles_idents_2.append(t_ident)
    print("include_ident_1:", t_ident)
    
    t_idents_1 = [i for i in idents_1 if t_ident in i]
    print("226 t_idents_1", t_idents_1)
    context_i1 = {}
    if len(t_idents_1) > 0:
        if len(t_idents_1) == 1:
            t_ids = t_idents_1
            container_one = container
            container_one['link'] = f'https://openlibrary.org/borrow/ia/{t_ids[0]}?ref=ol'
            context_i1['cont'] = container_one
            print("233 context['cont']", context_i1['cont'])
            return context_i1
            # return Response(context, template_name='read_book.html', )
        elif len(t_idents_1) > 1:
            containers_many = []
            t_ids = t_idents_1
            links = [f'https://openlibrary.org/borrow/ia/{ident}?ref=ol' for ident in t_ids]
            for link in links:
                container_many = container
                container_many['link'] = link
                containers_many.append(container_many)

                context_i1['conts'] = containers_many
                print("245 context['conts'][0]", context_i1['conts'][0])
            return context_i1
            # return Response(context, template_name='read_book.html', )
    
    else:
        print("NO include_ident_1")
        text ="no context"
        return text

def include_ident_2(idents_1, titles_idents_2, container, context):

    t_ident = titles_idents_2[-1]
    print("include_ident_2:", t_ident)
    t_idents_2 = [i for i in idents_1 if i[:i.index("00")] in t_ident]
    print("253 t_idents_2", t_idents_2)
    context_i2 = {}
    if len(t_idents_2) > 0:
        if len(t_idents_2) == 1:
            t_ids = t_idents_2
            container_one = container
            container_one['link'] = f'https://openlibrary.org/borrow/ia/{t_ids[0]}?ref=ol'
            context_i2['cont'] = container_one
            print("context['cont']", context_i2['cont'])
            return context_i2
            # return Response(context, template_name='read_book.html', )
        elif len(t_idents_2) > 1:
            containers_many = []
            t_ids = t_idents_2
            links = [f'https://openlibrary.org/borrow/ia/{ident}?ref=ol' for ident in t_ids]
            for link in links:
                container_many = container
                container_many['link'] = link
                containers_many.append(container_many)

                context_i2['conts'] = containers_many
                print("context['conts'][0]", context_i2['conts'][0])
            return context_i2
            # return Response(context, template_name='read_book.html', )
    else:
        print("NO include_ident_2")
        text ="no context"
        return text


def idents_title_author_1(idents_title_1, indets_author_1):
    ids = list(set(idents_title_1 + indets_author_1))
    context_ta = {}
    if len(ids) == 1:
        container_one = container
        container_one['link'] = f'https://openlibrary.org/borrow/ia/{ids[0]}?ref=ol'
        context_ta['cont'] = container_one
        print("context['cont']", context_ta['cont'])
        return context_ta
        # return Response(context, template_name='read_book.html', )
    elif len(ids) > 1:
        containers_many = []
        links = [f'https://openlibrary.org/borrow/ia/{ident}?ref=ol' for ident in ids]
        for link in links:
            container_many = container
            container_many['link'] = link
            containers_many.append(container_many)

        context_ta['conts'] = containers_many
        print("context['conts'][0]", context_ta['conts'][0])
        return context_ta
        # return Response(context, template_name='read_book.html', )
    else:
        print("NO idents_title_author")
        text ="no context"
        return text

def idents_title_author_2(idents_title_2, indets_author_2):
    ids = list(set(idents_title_2 + indets_author_2))
    context_ta = {}
    if len(ids) == 1:
        container_one = container
        container_one['link'] = f'https://openlibrary.org/borrow/ia/{ids[0]}?ref=ol'
        context_ta['cont'] = container_one
        print("context['cont']", context_ta['cont'])
        return context_ta
        # return Response(context, template_name='read_book.html', )
    elif len(ids) > 1:
        containers_many = []
        links = [f'https://openlibrary.org/borrow/ia/{ident}?ref=ol' for ident in ids]
        for link in links:
            container_many = container
            container_many['link'] = link
            containers_many.append(container_many)

        context_ta['conts'] = containers_many
        print("context['conts'][0]", context_ta['conts'][0])
        return context_ta
        # return Response(context, template_name='read_book.html', )
    else:
        print("NO idents_title_author")
        text ="no context"
        return text


def use_title(context, formlib, book, identities_1, idents_title_1, idents_author_1, idents_1, titles_idents_1, identities):
    # identities_1a = []
    parameters = ""

    titles_split = []
    titles_short = []
    titles_split_q = []
    titles_short_q = []
    titles_plus = []
    titles_plus_q = []

    idents = []
    # idents.clear()

    idents_title = []
    # idents_title.clear()

    idents_author = []
    # idents_author.clear()

    titles_jsplit = []
    titles_jshort = []
    authors_jname = []
    authors_jsurname = []

    if formlib.is_valid():
        
        title_to_search = book.title
        title_to_search_split = title_to_search.lower().replace("the ", "").replace(":", "").split()
        auth_to_search = book.author
        author_to_search = auth_to_search.lower()
        auth_surname = book.surname
        author_surname = auth_surname.lower()
        print('title_to_search', title_to_search)

        title_to_search_q = title_to_search.lower().replace("the ", "").replace("-", "slugify")
        title_slugify_q = slugify(title_to_search_q).replace("-", " ").replace("slugify", "-")
        title_split_q = title_slugify_q.split()
        author_to_search_q = author_to_search.replace("-", "slugify")
        author_slugify_q = slugify(author_to_search_q).replace("-", " ").replace("slugify", "-")
        author_split_q = author_slugify_q.split()
        auth_surname_q = author_surname.replace("-", "slugify")
        author_surname_slugify_q = slugify(auth_surname_q).replace("-", " ").replace("slugify", "-")
        author_surname_q = author_surname_slugify_q

        if len(title_to_search_split) > 5:
            title_split_short = title_to_search_split[:5]
            titles_split.append(title_split_short)
            title_split_short_q = title_split_q[:5]
            titles_split_q.append(title_split_short_q)
            title_short = " ".join(title_split_short)
            titles_short.append(title_short)
            title_short_q = " ".join(title_split_short_q)
            #title_ident = "".join(title_split_short_q)
            titles_idents_1.append("".join(title_split_short_q))
            title_plus = title_short.replace(' ', '+')
            titles_plus.append(title_plus)
            title_plus_q = title_short_q.replace(' ', '+')
            titles_plus_q.append(title_plus)
            print('if title_plus', title_plus)
        else:
            title_split_short = title_to_search_split
            titles_split.append(title_split_short)
            title_short = " ".join(title_split_short)
            titles_short.append(title_short)
            title_plus = title_short.replace(' ', '+')
            titles_plus.append(title_plus)
            print('else title_plus', title_plus)
            title_split_short_q = title_split_q
            titles_split.append(title_split_short_q)
            titles_idents_1.append("".join(title_split_short_q))
            title_short_q = " ".join(title_split_short_q)
            titles_short_q.append(title_short_q)
            title_plus_q = title_slugify_q.replace(' ', '+')
            titles_plus_q.append(title_plus_q)

        # parameters = f'{title_plus}+{author_surname}'
        # parameters = f'{title_plus_q}+{author_surname_q}'
        parameters = f'{title_plus_q}'
        print('parameters:', parameters)
        search_url = f'https://openlibrary.org/search/inside.json?q={parameters}'
        print('search_url', search_url)
        # search_url = f'https://openlibrary.org/search/inside.json?q={title_plus}'
        r = requests.get(url=search_url)
        if r.status_code != 200:
            context['message_read'] = f'Sorry, probably something went wrong, r.status_code = {r.status_code}'
            return Response(context, template_name='read_book.html', )

        data = r.json()
        # data = r
        # records = json.loads(data)
        records = data
        links = []

        # url = 'https://openlibrary.org/account/login'
        # context['searching'] = url

        # url = 'https://archive.org/account/login'
        # url = 'https://openlibrary.org/account/login'
        # searching = f'{url}'
        
        # idents = []
        # idents_title = []
        # idents_author = []
        # titles_jsplit = []
        # titles_jshort = []
        # authors_jname = []
        # authors_jsurname = []
        
        if records['hits']['hits']:
            recs = records['hits']['hits']
            print('len(recs)', len(recs))
            n_records = len(recs)
            print('titles_short[-1]', titles_short[-1])
            # for i in range(n_records-1):
            for i in range(n_records):
                try:
                    if recs[i]['edition']['ocaid']:
                        ident = recs[i]['edition']['ocaid']
                        idents.append(ident)
                except Exception as e:
                    print(f"151 {e}, i: {i}")
                    
                try:
                    if recs[i]['edition']['title']:
                        title_jshort = recs[i]['edition']['title'].lower()
                        # print('title_jshort', title_jshort)
                        # print('titles_short[0]', titles_short[0])
                        titles_jshort.append(title_jshort)
                        title_jsplit = title_jshort.split()
                        titles_jsplit.append(title_jsplit)

                        if title_jshort==title_short or set(title_jsplit).issubset(set(title_split_short)) or set(title_split_short).issubset(set(title_jsplit)):
                            idents_title.append(idents[-1])
                        # if title_jshort==titles_short[0] set(title_jsplit).issubset(set(titles_split[0])) or set(titles_split[0]).issubset(set(title_jsplit)):
                        #     idents_title.append(idents[-1])

                        else:
                            print('1. no title')
                    else:
                        print('2. no title')
                except Exception as e:
                    print(f"168 {e}, i: {i}")
                try:
                    if recs[i]['edition']['authors'][0]['name']:
                        author_jname = recs[i]['edition']['authors'][0]['name'].lower()
                        authors_jname.append(author_jname)
                        author_jsurname = author_jname.split()[-1]
                        authors_jsurname.append(author_jsurname)
                        if author_jname == author_to_search or author_jsurname == author_surname:
                            idents_author.append(idents[-1])
                        else:
                            print('1. no author')
                            
                    else:
                        print('2. no author')
                        
                except Exception as e:
                    print(f"180 {e}, i: {i}")

            print('163 idents', idents)
            # print('idents_title', idents_title)
            # print('idents_author', idents_author)

            if idents and idents_title and idents_author:
                identities_list_1 = list(set(idents).intersection(set(idents_title).intersection(set(idents_author))))
                # identities.extend(identities_list_1)
                if len(identities_list_1) > 0:
                    identities_1.extend(identities_list_1)
                    print('identities_list_1', identities_list_1)
                    identities.extend(identities_list_1)
                    
                else:
                    print('1. no links')

            elif idents and idents_title and not idents_author:
                identities_list_2 = list(set(idents).intersection(set(idents_title)))
                # identities.extend(identities_list_2)
                if len(identities_list_2) > 0:
                    identities_1.extend(identities_list_2)
                    print('identities_list_2', identities_list_2)
                    identities.extend(identities_list_2)
                else:
                    print('2. no links')
                    idents_title_1.extend(idents_title)

            elif idents and idents_author and not idents_title:
                identities_list_3 = list(set(idents).intersection(set(idents_title)))
                # identities.extend(identities_list_3)
                if len(identities_list_3) > 0:
                    identities_1.extend(identities_list_3)
                    print('identities_list_3', identities_list_3)
                    identities.extend(identities_list_3)
                else:
                    print('19 3. no links')
                    idents_author_1.extend(idents_author)
                    idents_1.extend(idents)



            else:
                print('4 no links')
                
                #context['message'] = 'Sorry, probably no free ebook on this title'
                #return Response(context, template_name='read_book.html', )

        else:
            print('5 no links')
            text ="no context"
            return text

            #context['message'] = 'Sorry, probably there is no this book to read for free'
            #return Response(context, template_name='read_book.html', )    
        # return identities

def use_meta_title_author(context, formlib, book, identities_2, idents_title_2, idents_author_2, idents_2, identities):
    # identities = []
    titles_split_f = []
    titles_short_f = []
    titles_split_q_f = []
    titles_short_q_f = []
    titles_plus = []
    titles_plus_q = []
    idents = []
    # idents.clear()
    idents_title = []
    idents_author = []
    # titles_jsplit = []
    titles_jsplit_f = []
    # titles_jshort = []
    titles_jshort_f = []
    authors_jname = []
    authors_jsurname = []

    if formlib.is_valid():        
        title_to_search = book.title
        title_to_search_split = title_to_search.lower().replace(":", "").replace("the ", "").split()
        auth_to_search = book.author
        author_to_search = auth_to_search.lower()
        auth_surname = book.surname
        author_surname = auth_surname.lower()
        print('title_to_search', title_to_search)

        title_to_search_q = title_to_search.lower().replace("the ", "").replace("-", "slugify")
        title_slugify_q = slugify(title_to_search_q).replace("-", " ").replace("slugify", "-")
        title_split_q = title_slugify_q.split()
        author_to_search_q = author_to_search.replace("-", "slugify")
        author_slugify_q = slugify(author_to_search_q).replace("-", " ").replace("slugify", "-")
        author_split_q = author_slugify_q.split()
        auth_surname_q = author_surname.replace("-", "slugify")
        author_surname_slugify_q = slugify(auth_surname_q).replace("-", " ").replace("slugify", "-")
        author_surname_q = author_surname_slugify_q

        if len(title_to_search_split) > 5:
            title_split_short_f = title_to_search_split[:5]
            titles_split_f.append(title_split_short_f)
            title_split_short_q_f = title_split_q[:5]
            titles_split_q_f.append(title_split_short_q_f)
            title_short_f = " ".join(title_split_short_f)
            titles_short_f.append(title_short_f)
            title_short_q_f = " ".join(title_split_short_q_f)
            title_plus_q = title_short_q_f.replace(' ', '+')
            titles_plus_q.append(title_plus_q)
            print('if title_plus_q', title_plus_q)
        else:
            title_split_short_f = title_to_search_split
            titles_split_f.append(title_split_short_f)
            title_short_f = " ".join(title_split_short_f)
            titles_short_f.append(title_short_f)
            # title_plus_q = title_short.replace(' ', '+')
            # titles_plus.append(title_plus)
            
            title_split_short_q_f = title_split_q
            titles_split_q_f.append(title_split_short_q_f)
            title_short_q_f = " ".join(title_split_q)
            titles_short_q_f.append(title_short_q_f)
            title_plus_q = title_short_q_f.replace(' ', '+')
            titles_plus_q.append(title_plus_q)
            print('else title_plus_q', title_plus_q)
            print('else title_short_q_f', title_short_q_f)

        # parameters = f'{title_plus}+{author_surname}'
        parameters = f'{title_plus_q}+{author_surname_q}'
        print('parameters:', parameters)
        search_url = f'https://openlibrary.org/search/inside.json?q={parameters}'
        print('search_url', search_url)
        # search_url = f'https://openlibrary.org/search/inside.json?q={title_plus}'
        r = requests.get(url=search_url)
        if r.status_code != 200:
            context['message_read'] = f'Sorry, probably something went wrong, r.status_code = {r.status_code}'
            return Response(context, template_name='read_book.html', )

        data = r.json()
        # data = r
        # records = json.loads(data)
        records = data
        links = []

        # url = 'https://openlibrary.org/account/login'
        # context['searching'] = url

        # url = 'https://archive.org/account/login'
        # url = 'https://openlibrary.org/account/login'
        # searching = f'{url}'
        
        # idents = []
        # idents_title = []
        # idents_author = []
        # titles_jsplit = []
        # titles_jshort = []
        # authors_jname = []
        # authors_jsurname = []
        
        if records['hits']['hits']:
            recs = records['hits']['hits']
            print('len(recs)', len(recs))
            n_records = len(recs)
            print('titles_short_f[-1]', titles_short_f[-1])
            for i in range(n_records):
                try:
                    if recs[i]['edition']['ocaid']:
                        ident = recs[i]['edition']['ocaid']
                        idents.append(ident)
                        
                except Exception as e:
                    print(f"151 {e}, i: {i}")
                    
                try:
                    if len(recs[i]['fields']['meta_title']) > 0:
                        title_jshort_f = str(recs[i]['fields']['meta_title'][0].lower())
                        title_jshort_f_s = title_jshort_f.replace("-", "slugify")
                        title_jshort_f_slugify = slugify(title_jshort_f).replace("-", " ").replace("slugify", "-")
                
                        # print('title_jshort_f', title_jshort_f)
                        # print('titles_short[0]', titles_short[0])
                        titles_jshort_f.append(title_jshort_f)
                        title_jsplit_f = title_jshort_f.split()
                        titles_jsplit_f.append(title_jsplit_f)

                        
                        # print('342 title_short_q_f', title_jshort_f_slugify)
                        # print('342 title_short_q_f', title_short_q_f)
                        if title_jshort_f==title_short_f or title_jshort_f_slugify==title_short_q_f or set(title_jsplit_f).issubset(set(title_split_short_f)) or set(title_split_short_f).issubset(set(title_jsplit_f)):
                            print("title_jshort_f: ", title_jshort_f)
                            idents_title.append(idents[-1])
                        # if title_jshort==titles_short[0] set(title_jsplit).issubset(set(titles_split[0])) or set(titles_split[0]).issubset(set(title_jsplit)):
                        #     idents_title.append(idents[-1])

                        else:
                            print('1. no title')
                    else:
                        print('2. no title')
                except Exception as e:
                    print(f"168 {e}, i: {i}")
                try:
                    if recs[i]['edition']['authors'][0]['name']:
                        author_jname = recs[i]['edition']['authors'][0]['name'].lower()
                        authors_jname.append(author_jname)
                        author_jsurname = author_jname.split()[-1]
                        authors_jsurname.append(author_jsurname)
                        if author_jname == author_to_search or author_jsurname == author_surname:
                            idents_author.append(idents[-1])
                        else:
                            print('1. no author')
                            
                    else:
                        print('2. no author')
                      
                except Exception as e:
                    print(f"180 {e}, i: {i}")
            # idents_2.extend(idents) 
            #  
            # print('idents', idents)
            # print('idents_title', idents_title)
            # print('idents_author', idents_author)

            if idents and idents_title and idents_author:
                identities_list_1 = list(set(idents).intersection(set(idents_title).intersection(set(idents_author))))
                # identities.extend(identities_list_1)
                if len(identities_list_1) > 0:
                    identities_2.extend(identities_list_1)
                    print('identities_list_1', identities_list_1)
                    
                else:
                    print('1. no links')
                    

            elif idents and idents_title and not idents_author:
                identities_list_2 = list(set(idents).intersection(set(idents_title)))
                # identities.extend(identities_list_2)
                if len(identities_list_2) > 0:
                    identities_2.extend(identities_list_2)
                    print('identities_list_2', identities_list_2)
                else:
                    print('2. no links')
                    idents_title_2.extend(idents_title)

            elif idents and idents_author and not idents_title:
                identities_list_3 = list(set(idents).intersection(set(idents_title)))
                # identities.extend(identities_list_3)
                if len(identities_list_3) > 0:
                    identities_2.extend(identities_list_3)
                    print('identities_list_3', identities_list_3)
                else:
                    print('498 3. no links')
                    idents_author_2.extend(idents_title)

            else:
                print('4 no links')
                #context['message'] = 'Sorry, probably no free ebook on this title'
                #return Response(context, template_name='read_book.html', )

        else:
            print('NO LINKS use_meta_title')
            text ="no context"
            return text
            # context['message'] = 'Sorry, probably there is no this book to read for free'
            # return Response(context, template_name='read_book.html', )    
        # return identities


