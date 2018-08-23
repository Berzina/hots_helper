ROW_PATTERN = """
<p>
  <blockquote>{talent.level} -- {talent.name}</blockquote>
  <figure> <img src="{talent.img}"/>
    <figcaption>
      <i>{talent.descr}</i>
    </figcaption>
  </figure>
</p>
"""

PAGE = """
  <figure> <img src="{hero.image}"/>
    <figcaption>
      <i>{hero.stats}</i>
    </figcaption>
  </figure>

  <h3>{build.name}</h3>

  {rows}

"""

EMODJI_NUMBER_MAPPING = {
  1: '1️⃣',
  3: '3️⃣',
  4: '4️⃣',
  6: '6️⃣',
  7: '7️⃣',
  9: '9️⃣',
  10: '1️⃣0️⃣',
  12: '1️⃣2️⃣',
  13: '1️⃣3️⃣',
  15: '1️⃣5️⃣',
  16: '1️⃣6️⃣',
  19: '1️⃣9️⃣',
  20: '2️⃣0️⃣'
}
