import os
import click
import json
import re 

@click.command()
@click.option('--shelf', help='shelf from goodreads')
@click.option('--user_id', help='user to scrape from')
def main(shelf, user_id):
    # os.system(f'cd ./GoodreadsScraper && python crawl.py my-books --shelf={shelf} --user_id={user_id}')

    data = []
    book_id = []

    with open(f'./GoodreadsScraper/book_{user_id}.jl', 'r') as file:
        for line in file.readlines():
            json_line = json.loads(line)
            data.append(json_line)
            book_id.append(re.search('show\/(.*)', json_line["url"])[1] )

    with open(f'./temp/book_{user_id}.json', "w") as outfile:
        json.dump(data, outfile)

    with open(f'./temp/book_{user_id}.txt', 'w') as outfile:
        for id in book_id:
            outfile.write(id + '\n')

    crawl_command = """
    python get_reviews.py --book_ids_path ../temp/{}.txt --output_directory_path ../temp/ --browser chrome --format json
    """.format('book_' + user_id)

    os.system(f'cd goodreads-scraper && {crawl_command}')
    
    

if __name__ == '__main__':
    main()