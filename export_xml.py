from datetime import datetime

from bs4 import BeautifulSoup

from src.models import Url
from src import config


class Xml:
    template_path = config.XML_TEMPLATE_PATH

    def __init__(self):
        if not self.template_path.exists():
            raise Exception('Template does not exist')

    @staticmethod
    def get_export_file(counter):
        """Gets export file path

        :param counter: iteration count
        :return: file_path
        :rtype: Path
        """
        file_name = 'sitemap_{}_{}.xml'.format(
            datetime.now().strftime('%Y%m%d'),
            counter,
        )
        file_path = config.EXPORT_DIR.child(file_name)
        return file_path

    @staticmethod
    def chunks(l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def generate_xml(self):
        """Generate an XML

        Write the elements in-memory first and then write to file.
        """
        print('This may take a few seconds. Please be patient.')

        urls = Url.select().where(
            Url.url.startswith('https://www.natureasia.com'),
        ).order_by(
            Url.url.asc(),
        )
        if urls:
            counter = 0
            for chunk in self.chunks(urls, 50000):
                """Example
                <url>
                    <loc>http://www.natureasia.com</loc>
                    <priority>1.00</priority>
                </url>
                """
                counter += 1

                # Find 'urlset' element inside the XML template
                with open(self.template_path, 'r') as f:
                    xml = f.read()

                xml = BeautifulSoup(xml, 'xml')
                urlset_tag = xml.find('urlset')

                # Loop through each batch. 1 batch == 1 xml
                for url in chunk:
                    # Make URL tag
                    url_tag = self.make_url_tag(url)

                    # Append it to the urlset tag
                    urlset_tag.append(url_tag)

                # Insert content to template and write to file
                export_path = self.get_export_file(counter)
                with open(export_path, 'w') as f:
                    content = xml.prettify(formatter='xml')
                    f.write(content)
                print('Exported {}!'.format(export_path))

    @staticmethod
    def make_url_tag(url):
        """Make an URL tag (Beautiful Soup)

        :param url: Url object
        :return: url tag
        :rtype: BeautifulSoup
        """
        # Create XML elements via BeautifulSoup
        soup = BeautifulSoup('', 'xml')

        # Create URL tag
        url_tag = soup.new_tag('url')

        # Create 'loc' tag and append to 'url' tag
        loc_tag = soup.new_tag('loc')
        loc_tag.insert(0, url.url)
        url_tag.insert(0, loc_tag)

        # Create 'priority' tag and append to 'url' tag
        if url.priority:
            priority_tag = soup.new_tag('priority')
            priority_tag.append('{0:.2f}'.format(url.priority))
            url_tag.insert(1, priority_tag)

        return url_tag


if __name__ == '__main__':
    Xml().generate_xml()
    print('Finished!')
