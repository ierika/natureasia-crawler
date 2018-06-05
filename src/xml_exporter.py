import os
from datetime import datetime

from unipath import Path

from models import Url


class Xml:
    template_path = Path(__file__).ancestor(1).child('sitemap_template.xml')

    def __init__(self):
        if not self.template_path.exists():
            raise Exception('Template does not exist')

    @staticmethod
    def get_export_file(counter):
        file_name = 'sitemap_{}_{}.xml'.format(
            datetime.now().strftime('%Y%m%d'),
            counter,
        )
        file_path = Path(os.environ.get('HOME'), 'Downloads', file_name)
        return file_path

    @staticmethod
    def chunks(l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def generate_xml(self):
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
                xml_content = ''
                counter += 1

                # Loop through each batch. 1 batch == 1 xml
                for url in chunk:
                    loc = '<loc>{}</loc>'.format(url.url)
                    priority = ''
                    if url.priority:
                        priority = '<priority>{0:.2f}</priority>'.format(
                            url.priority,
                        )
                    url_block = '<url>{loc}{priority}</url>'.format(
                        loc=loc,
                        priority=priority,
                    )
                    xml_content += url_block

                # Extract template text
                with open(self.template_path, 'r') as f:
                    template = f.read().encode('utf-8')
                    template = template.decode('utf-8').strip()

                # Insert content to template and write to file
                export_path = self.get_export_file(counter)
                with open(export_path, 'w') as f:
                    content = template.replace('{content}', xml_content)
                    f.write(content)
                print('Exported {}!'.format(export_path))


if __name__ == '__main__':
    Xml().generate_xml()
    print('Finished!')
