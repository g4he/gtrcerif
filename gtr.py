import requests, json, datetime

def get(url):
    resp = requests.get(url)
    body = resp.text
    return json.loads(body)
    #xml = etree.fromstring(resp.text.encode("utf-8"))
    
def get_project(identifier):
    raw = get("http://gtr.rcuk.ac.uk/cerif/cfproj/" + identifier)
    return Project(raw['cfClassOrCfClassSchemeOrCfClassSchemeDescr'][0])

def get_fund(identifier):
    raw = get("http://gtr.rcuk.ac.uk/cerif/cffund/" + identifier)
    return Fund(raw['cfClassOrCfClassSchemeOrCfClassSchemeDescr'][0])

def get_org(identifier):
    raw = get("http://gtr.rcuk.ac.uk/cerif/cforgunit/" + identifier)
    return Org(raw['cfClassOrCfClassSchemeOrCfClassSchemeDescr'][0])
    
def get_person(identifier):
    raw = get("http://gtr.rcuk.ac.uk/cerif/cfpers/" + identifier)
    return Person(raw['cfClassOrCfClassSchemeOrCfClassSchemeDescr'][0])

class Cerif(object):
    def __init__(self, raw):
        self.raw = raw
    
    def start(self):
        s = self.raw.get("cfStartDate")
        if s is not None:
            dt = datetime.datetime.fromtimestamp(s / 1000)
            return datetime.datetime.strftime(dt, "%d %B %Y")
        return None
        
    def end(self):
        s = self.raw.get("cfEndDate")
        if s is not None:
            dt = datetime.datetime.fromtimestamp(s / 1000)
            return datetime.datetime.strftime(dt, "%d %B %Y")
        return None
    
    def json(self):
        return json.dumps(self.raw, indent=2)

class Person(Cerif):
    def name(self):
        for obj in self.raw.get("cfResIntOrCfKeywOrCfPersPers", []):
            if obj.get("name", "").endswith("cfPersName_Pers"):
                first = obj.get("value", {}).get("cfFirstNames", "")
                last = obj.get("value", {}).get("cfFamilyNames", "")
                return first + " " + last
        return None
        
    def orgs(self):
        os = []
        for obj in self.raw.get("cfResIntOrCfKeywOrCfPersPers", []):
            if obj.get("name", "").endswith("cfPers_OrgUnit"):
                v = obj.get("value", {}).get("cfOrgUnitId", "")
                if v is not None and v != "":
                    os.append(v)
        return os
        
    def projects(self):
        os = []
        for obj in self.raw.get("cfResIntOrCfKeywOrCfPersPers", []):
            if obj.get("name", "").endswith("cfProj_Pers"):
                v = obj.get("value", {}).get("cfProjId", "")
                if v is not None and v != "":
                    os.append(v)
        return os

class Org(Cerif):
    def name(self):
        for obj in self.raw.get("cfNameOrCfResActOrCfKeyw", []):
            if obj.get("name", "").endswith("cfName"):
                return obj.get("value", {}).get("value", "")
        return None
        
    def headcount(self):
        return self.raw.get("cfHeadcount", 0)

class Fund(Cerif):
    def amount(self):
        return self.raw.get("cfAmount", 0)
    
    def orgs(self):
        os = []
        for obj in self.raw.get("cfNameOrCfDescrOrCfKeyw", []):
            if obj.get("name", "").endswith("cfOrgUnit_Fund"):
                v = obj.get("value", {}).get("cfOrgUnitId", "")
                if v is not None and v != "":
                    os.append(v)
        return os
    
    def projects(self):
        os = []
        for obj in self.raw.get("cfNameOrCfDescrOrCfKeyw", []):
            if obj.get("name", "").endswith("cfProj_Fund"):
                v = obj.get("value", {}).get("cfProjId", "")
                if v is not None and v != "":
                    os.append(v)
        return os

class Project(Cerif):
    def title(self):
        for obj in self.raw.get("cfTitleOrCfAbstrOrCfKeyw", []):
            if obj.get("name", "").endswith("cfTitle"):
                return obj.get("value", {}).get("value", "")
        return None
    
    def abstract(self):
        for obj in self.raw.get("cfTitleOrCfAbstrOrCfKeyw", []):
            if obj.get("name", "").endswith("cfAbstr"):
                return obj.get("value", {}).get("value", "")
        return None
        
    def funding(self):
        fundings = []
        for obj in self.raw.get("cfTitleOrCfAbstrOrCfKeyw", []):
            if obj.get("name", "").endswith("cfProj_Fund"):
                v = obj.get("value", {}).get("cfFundId", "")
                if v is not None and v != "":
                    fundings.append(v)
        return fundings
    
    def orgs(self):
        os = []
        for obj in self.raw.get("cfTitleOrCfAbstrOrCfKeyw", []):
            if obj.get("name", "").endswith("cfProj_OrgUnit"):
                v = obj.get("value", {}).get("cfOrgUnitId", "")
                if v is not None and v != "":
                    os.append(v)
        return os
        
    def people(self):
        os = []
        for obj in self.raw.get("cfTitleOrCfAbstrOrCfKeyw", []):
            if obj.get("name", "").endswith("cfProj_Pers"):
                v = obj.get("value", {}).get("cfPersId", "")
                if v is not None and v != "":
                    os.append(v)
        return os
    
