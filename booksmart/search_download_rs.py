import requests
from bs4 import BeautifulSoup

# WHY
# The SearchRequest module contains all the internal logic for the library.
#
# This encapsulates the logic,
# ensuring users can work at a higher level of abstraction.

# USAGE
# req = search_request.SearchRequest("[QUERY]", search_type="[title]")


class SearchRequestRS:

    col_names = [
        "ID",
        "Author(s)",
        "Title",
        "Publisher",
        "Year",
        "Pages",
        "Language",
        "Size",
        "Extension",
        "Mirrors",
        "Edit",
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
               
                f"https://libgen.rs/index.php?req={query_parsed}&column=title"
            )
        elif self.search_type.lower() == "author":
            search_url = (
                
                f"https://libgen.rs/index.php?req={query_parsed}&column=author"
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
            information_table_1 = soup.find_all("table")[1]
            information_table_2 = soup.find_all("table")[2]
        except Exception as e:
            print(f"exception: {e}")

        output_datas = {}
        # try:
        #     raw_data_my = [ 
        #         [
        #             [a.get('href') for a in td.find_all("a")]
        #             if td.find("a")
        #             and td.find("a").has_attr("title")
        #             and td.find("a")["title"] != ""
        #             else "".join(td.stripped_strings)
        #             for td in row.find_all("td")
        #         ]
        #         for row in information_table.find_all("tr")[
        #             1:
        #         ]  # Skip row 0 as it is the headings row
        #     ]

        #     try:
        #         output_data_my = [dict(zip(self.col_names, row)) for row in raw_data_my]
                
        #         # output_datas["output_data_my"] = output_data_my
        #         print("\noutput_data_my =", output_data_my)
        #         # if output_data_my:
        #         #     output_data_my_dict = {"output_data_my": output_data_my}
        #         #     output_datas.append(output_data_my_dict)
                    
        #         # else: 
        #         #     print("else NO output_data_my")
        #         # print("output_data_my", output_data_my)
        #         # print("output_data_a =", output_data_a)   
        #         # return output_data_my
        #     except:
        #         print("except NO output_data_my")
        # except:
        #         print("except NO raw_data_a")
                
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
                for row in information_table_1.find_all("tr")[
                    1:
                ]  # Skip row 0 as it is the headings row
            ]
            try:        
                output_data_all = [dict(zip(self.col_names, row)) for row in raw_data]
                if output_data_all:
                    
                    if len(output_data_all) < 3:
                        output_data = output_data_all
                        print('1. output_data =', output_data)
                        return output_data
                    else:
                        output_data = output_data_all[:2]
                        print('1. output_data =', output_data)
                        return output_data
                else:
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
                            for row in information_table_2.find_all("tr")[
                                1:
                            ]  # Skip row 0 as it is the headings row
                        ]
                        try:        
                            output_data_all = [dict(zip(self.col_names, row)) for row in raw_data]
                            
                            if len(output_data_all) < 3:
                                output_data = output_data_all
                                print('1. output_data =', output_data)
                                return output_data
                            else:
                                output_data = output_data_all[:2]
                                print('1. output_data =', output_data)
                                return output_data
                        except:
                            print("2. except NO output_data information_table_1")
                    except:
                        print("2. except NO raw_data")

            except:
                print("1. except NO output_data information_table_1")
        except:
            print("1. except NO raw_data")

        

# def aggregate_request_data_my(self):
#         search_page = self.get_search_page()
#         soup = BeautifulSoup(search_page.text, "html.parser")
#         self.strip_i_tag_from_soup(soup)

#         # Libgen results contain 3 tables
#         # Table2: Table of data to scrape.
#         try:
#             information_table = soup.find_all("table")[1]
#         except Exception as e:
#             print(f"exception: {e}")

        # try:
        #     raw_data_my = [ 
        #         [
        #             [a.get('href') for a in td.find_all("a")]
        #             if td.find("a")
        #             and td.find("a").has_attr("title")
        #             and td.find("a")["title"] != ""
        #             else "".join(td.stripped_strings)
        #             for td in row.find_all("td")
        #         ]
        #         for row in information_table.find_all("tr")[
        #             1:
        #         ]  # Skip row 0 as it is the headings row
        #     ]
          
        #     try:
        #         output_data_my = [dict(zip(self.col_names, row)) for row in raw_data_my]
        #         print("\noutput_data_my =", output_data_my)
        #         # print("output_data_my", output_data_my)
        #         # print("output_data_a =", output_data_a)   
        #         # return output_data_my
        #     except:
        #         print("no output_data_a")
        # except:
        #         print("no raw_data_a")


class SearchRequestPM_my:

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

        try:
            raw_data_my = [ 
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
          

            try:
                output_data_my = [dict(zip(self.col_names, row)) for row in raw_data_my]
                print("\noutput_data_my =", output_data_my)
                # print("output_data", output_data)
                # print("output_data_a =", output_data_a)   
                return output_data_my
            except:
                print("no output_data_a")
        except:
                print("no raw_data_a")

