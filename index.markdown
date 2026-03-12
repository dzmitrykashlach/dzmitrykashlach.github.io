---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
---

{% for project in site.projects %}
  <h2> {{ project.title }} </h2>
  <p>{{ project.description }}</p>
{% endfor %}