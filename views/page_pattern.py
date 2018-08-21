STYLES = """
<style type="text/css">

  body {{font-family: "Open Sans",sans-serif;}}

  h1 {{margin-bottom: 5pt;}}
  h2 {{margin-top: 26pt;}}

  #main-table {{max-width: 540px;
               table-layout: fixed;
               text-align:center;}}


  #main-table tr:nth-child(2n) {{background: #f0f0f0;}}

  #main-table tr:nth-child(1) {{background: #666;
                               color: #fff;}}

  #main-table td:nth-child(4) {{width: 65%;}}

  #stats {{font-style: italic;
          margin-top: 12pt;}}

  .talent_name {{font-style: italic;
                font-size: 11pt;
                color: green}}
</style>
"""

ROW_PATTERN = """
<p>
  <strong>{talent.level}</strong>|<strong>{talent.idx}</strong>|<strong>{talent.name}</strong><br/>
  ----------------------------
  <figure> <img src="http://blizzardheroes.ru{talent.img}"/>
    <figcaption>
      <i>{talent.descr}</i>
    </figcaption>
  </figure>
</p>
"""

PAGE = """
  <figure> <img src="http://happyzerg.ru{hero.image}"/>
    <figcaption>
      <i>{bhero.stats}</i>
    </figcaption>
  </figure>

  <h3>{build.name}</h3>

  {rows}

"""
