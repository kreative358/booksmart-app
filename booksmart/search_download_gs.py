import requests
from bs4 import BeautifulSoup

# WHY
# The SearchRequest module contains all the internal logic for the library.
#
# This encapsulates the logic,
# ensuring users can work at a higher level of abstraction.

# USAGE
# req = search_request.SearchRequest("[QUERY]", search_type="[title]")


class SearchRequestGS:

    col_names = [
        "ID Time add Title Series",
        "Author(s)",
        "Publisher",
        "Year",
        "Language",
        "Pages",
        "Size",
        "Ext.",
        "Mirror_1",
        "Mirror_2",
        "Mirror_3",
        "Mirror_4",
        "Mirror_5",
        "edit",
    ]

    def __init__(self, query, search_type="title"):
        self.query = query
        self.search_type = search_type

        if len(self.query) < 3:
            raise Exception("Query is too short")

    def strip_i_tag_from_soup(self, soup):
        subheadings = soup.find_all("i")
        for subheading in subheadings:
            subheading.decompose()

    def get_search_page(self):
        query_parsed = "%20".join(self.query.split(" "))
        if self.search_type.lower() == "title":
            search_url = (
                f"https://libgen.gs/index.php?req={query_parsed}&column=title"
            )
        elif self.search_type.lower() == "author":
            search_url = (
                f"https://libgen.gs/index.php?req={query_parsed}&column=author"
            )
        search_page = requests.get(search_url)
        return search_page

    def aggregate_request_data(self):
        search_page = self.get_search_page()
        soup = BeautifulSoup(search_page.text, "html.parser")
        self.strip_i_tag_from_soup(soup)

        # Libgen results contain 3 tables
        # Table2: Table of data to scrape.
        try:
            information_table = soup.find_all("table")[1]
        except Exception as e:
            print(f"exception: {e}")
        # print("information_table", information_table)

        # Determines whether the link url (for the mirror)
        # or link text (for the title) should be preserved.
        # Both the book title and mirror links have a "title" attribute,
        # but only the mirror links have it filled.(title vs title="libgen.io")

        # td_links_1 = [td.a["href"] for td.a["href"] in trs[-1]]
        # print("\ntd_links_1 =", td_links_1)
        # td_links_2 = trs[-1].find_all('a')
        # print("\ntd_links_2 =", td_links_2)
        # td_links_2 = trs[-1].find_all('a')
        # raw_data_1 = [
        #     [
        #         td.a["href"]
        #         if td.find("a")
        #         and td.find("a").has_attr("title")
        #         and td.find("a")["title"] != ""
        #         else "".join(td.stripped_strings)
        #         for td in row.find_all("td")
        #     ]
        #     for row in trs.find_all("td")
        #     ]  # Skip row 0 as it is the headings row

        try:
        
            raw_datas_a = [ 
                [
                    [a.get('href') for a in td.find_all("a")]
                    if td.find("a")
                    and td.find("a").has_attr("title")
                    and td.find("a")["title"] != ""
                    else "".join(td.stripped_strings)
                    for td in row.find_all("td")
                ]
                for row in information_table.find_all("tr")[
                    1:
                ]  # Skip row 0 as it is the headings row
            ]
            # print("raw_datas_a[0][-1] =", raw_datas_a[0][-1])
            # links_pdf = []
            # try:
                
            #     for raw_data_a in raw_datas_a:
            #         if raw_data_a[-2].value == "pdf":
            #             links_pdf.extend[raw_data_a[-1]]
            # except Exception as e:
            #     print(f"\nno links_pdf: reason {e}\n")
            # print("links_pdf =", links_pdf)

            try:
                output_datas_a = [dict(zip(self.col_names, row)) for row in raw_datas_a]
                # print("output_datas_a =", output_datas_a)
            # print("output_data", output_data)
                # print("output_data_a =", output_data_a)   
            except:
                print("no output_data_a")
        except:
                print("no raw_data_a")

        try:    
            raw_data = [
                [
                    td.a["href"]
                    if td.find("a")
                    and td.find("a").has_attr("title")
                    and td.find("a")["title"] != ""
                    else "".join(td.stripped_strings)
                    for td in row.find_all("td")
                ]
                for row in information_table.find_all("tr")[
                    1:
                ]  # Skip row 0 as it is the headings row
            ]
            try:        
                output_data = [dict(zip(self.col_names, row)) for row in raw_data]
                # print("raw_data[0][-1] =", raw_data[0][-1])
                print()
                # print("output_datas =", output_data)
                return output_data

            except:
                print("no output_data")
        except:
            print("np raw_data_")