def open_build(bh):

    builds_header = '''
* __{}__
```
---------------------------------
 lvl  | talent | talent name
      | idx    |
---------------------------------```'''

    builds_table = '''```
{:^6}|{:^8}|{:^16}
---------------------------------```
'''

    build_full_table = ''

    for build in bh.builds:
        build_full_table += builds_header.format(build.name)

        for talent in build.talents:
            build_full_table += builds_table.format(talent.level, talent.idx,
                                                    talent.name)

        build_full_table += '\n'

    return '''
**{name}**


{btable}
'''.format(name=bh.hero.name,
           btable=build_full_table)
