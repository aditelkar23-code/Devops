import yaml,sys
p='C:/Users/adity/OneDrive/Desktop/AWS Devops Projects/.github/workflows/deploy.yml'
try:
    with open(p,'r',encoding='utf-8') as f:
        yaml.safe_load(f)
    print('deploy.yml: ok')
except Exception as e:
    print('deploy.yml: parse error', e)
    sys.exit(1)
