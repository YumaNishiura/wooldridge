from io import StringIO
import sys
import re

import pandas as pd
import wooldridge
import mdpd

from type import Info 

datasets = [
    "401k", "401ksubs", "admnrev", "affairs", "airfare",
    "alcohol", "apple", "approval", "athlet1", "athlet2",
    "attend", "audit", "barium", "beauty", "benefits",
    "beveridge", "big9salary", "bwght", "bwght2", "campus",
    "card", "catholic", "cement", "census2000", "ceosal1",
    "ceosal2", "charity", "consump", "corn", "countymurders",
    "cps78_85", "cps91", "crime1", "crime2", "crime3",
    "crime4", "discrim", "driving", "earns", "econmath",
    "elem94_95", "engin", "expendshares", "ezanders", "ezunem",
    "fair", "fertil1", "fertil2", "fertil3", "fish",
    "fringe", "gpa1", "gpa2", "gpa3", "happiness",
    "hprice1", "hprice2", "hprice3", "hseinv", "htv",
    "infmrt", "injury", "intdef", "intqrt", "inven",
    "jtrain", "jtrain2", "jtrain3", "kielmc", "lawsch85",
    "loanapp", "lowbrth", "mathpnl", "meap00_01", "meap01",
    "meap93", "meapsingle", "minwage", "mlb1", "mroz",
    "murder", "nbasal", "nyse", "okun", "openness",
    "pension", "phillips", "pntsprd", "prison", "prminwge",
    "rdchem", "rdtelec", "recid", "rental", "return",
    "saving", "sleep75", "slp75_81", "smoke", "traffic1",
    "traffic2", "twoyear", "volat", "vote1", "vote2",
    "voucher", "wage1", "wage2", "wagepan", "wageprc",
    "wine",
]


def describe(name: str) -> str:

    tmp = sys.stdout
    result = StringIO()
    sys.stdout = result
    wooldridge.data(name, description=True)
    sys.stdout = tmp
    return result.getvalue()


def info(name: str) -> Info:

    desc = describe(name)
    lst = re.split(r"\n\s*\n", desc)

    # name, vars, obs
    sdesc = lst[0].split("\n")
    nvars = int(sdesc[1].split(": ")[1])
    nobs = int(sdesc[2].split(": ")[1])

    # data frame
    vars = mdpd.from_md(lst[1])

    # source
    src = lst[2]

    result = dict(name=name, nvars=nvars, nobs=nobs, src=src, vars=vars)

    return result
