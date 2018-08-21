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
<tr>
  <td>{talent.level}</td>
  <td>{talent.idx}</td>
  <td><img src="http://blizzardheroes.ru{talent.img}"/>
      <p class="talent_name">{talent.name}</p></td>
  <td>{talent.descr}</td>
"""

PAGE = """
<!DOCTYPE html>
<html>
<head>
  <title>{hero.en_name}</title>
</head>
<body>
  <table>
    <tr>
      <td>
        <img src="http://happyzerg.ru{hero.image}"/>
      </td>
      <td>
        <h1>{hero.name}</h1>
        <p id="stats">{bhero.stats}</p>
        <h2>{build.name}</h2>
      </td>
    </tr>
  </table>

  <table id="main-table">
    <tr>
      <td>Level</td>
      <td>Talent idx</td>
      <td>Image</td>
      <td>Description</td>
    </tr>
    {rows}
  </table>

</body>
</html>
"""
