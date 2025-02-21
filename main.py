from config import app_config

confluence = app_config.get_confluence()
model = app_config.get_llm()

space = "DS"
# Replace with your actual Confluence server URL and API token

# Get all pages from a space
# pages = confluence.get_all_pages_from_space(space)

# for page in pages:
#     print(f"Page Title: {page['title']}")
#     # Process page content as needed

page = confluence.get_page_by_title(space=space, title="Stream with Golden Gate (CDC)", expand="body.view")
# word = confluence.get_page_as_word(4344743802)
print(f"page: {page['title']}\n{page['body']['view']['value']}")
