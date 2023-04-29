import re

from csvbot import get_cols, log
from discord.ext import commands


class ParamMapper(commands.Converter):
    def parse(self, param_str):
        params = {}
        last_key = ""
        rest = ""
        for tok in re.split(r'[:=]', param_str):
            try:
                # split on last whitespace
                keyi = tok.rindex(' ')
                key = tok[keyi:].strip()
                rest = tok[:keyi].strip()
            except Exception as ex:
                log.debug(f"Exception: {ex}")
                log.debug(f'"last: {last_key}", "rest: {rest}"')

                # rest contains free-floating params, capture them
                if  len(rest) > 0:
                    params['none'] = rest

                # special end condition: no spaces in last segment
                key = tok.strip()
                rest = key

            # special end condition: last segment has a space, and key has the last segment
            # how can I detect before the split loop break? don't bother, just re-add? but lastkey has been updated.

            if last_key != "" and rest != "":
                params[last_key] = rest
                #print(f'"{last_key}", "{rest}"')
            last_key = key

        # condition breaking split-loop:
        # params contains everything correctly except last_key, which is supposed to be appended to the actual value of the last key.
        try:
            # edge conditions
            # param_str is empty, so no params
            if not param_str:
                log.debug("param_str is empty")
                return {} 
            elif len(params) == 0:
                # single param, return with 'none' to denote no args noted
                # 'none' should also grab any args without params
                log.debug(f"param_str is without params: {param_str}")
                return {'none': param_str}
            params[list(params)[-1]] = tok.strip()
        except Exception as ex:
            log.error(f"Error: {ex}")
            log.debug(f"params:{params}")
            log.debug(f"tok{tok}")
            log.debug(f"{last_key}")
            log.debug(f"{rest}")

        return params


    async def convert(self, ctx, argument):
        params = self.parse(argument)
        return params