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

ROW_PATTERN_2 = """
<p>
  <blockquote><strong>{talent.level}</strong> | <strong>{talent.idx}</strong> | {talent.title} ({talent.ability})</blockquote>
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
