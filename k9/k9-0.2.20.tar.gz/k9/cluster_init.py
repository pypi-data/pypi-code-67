import json
import os, time
import requests

from jinja2 import Environment, FileSystemLoader
from k9.helm import helm_install, helm_ls
from k9.core import namespace_exists, set_default_namespace, create_namespace, abs_path, list_pods, wait_for_pod


# util for jinja'ing XML
def write_templated_config(name: str, env, params):
    if not isinstance(params, dict):
        params = vars(params)
    template = env.get_template(name)
    template_body = template.render()
    if not os.path.exists('./.output/config'):
        if not os.path.exists('./.output'):
            os.mkdir('./.output')
        os.mkdir('./.output/config')
    path = f'./.output/config/{name}'
    
    f = open(path, 'w+')
    f.write(template_body)
    f.close()
    return f'./.output/config/{name}'


def install_jenkins(params: dict, namespace = 'cluster-tools'):
    """
    Installs Jenkins to the current kubernetes environment.

    :param params: a dictionary containing the params to insert into the jenkins chart's values.yaml
    :param namespace: the namespace to install jenkins in. defaults to cluster-tools
    :return: True on success, exception if failure.
    """
    set_default_namespace(namespace)
    if not namespace_exists(namespace):
        create_namespace(namespace)

    # get sonarqube token - todo
    sonarqube_token = 'asdf'
    params['sonarqube_token'] = sonarqube_token
    
    ns_ls = helm_ls(namespace)
    # install chart
    helm_install('simoncomputing/jenkins', params, release_name = 'jenkins', values_path = abs_path('yaml/jenkins-values.yml'), namespace = namespace)
    # get pod
    time.sleep(1)
    pods = list_pods(namespace)
    jenkins_pod = False
    for p in pods:
        if p.get('name', '').find('jenkins') != -1:
            jenkins_pod = p.get('name', False)
    # wait for pod to be ready
    if not wait_for_pod(jenkins_pod, namespace, timeout = 300):
        raise('Jenkins pod did not ready within 5 minutes. Please verify that your params are complete and correct.')
    return True
    

def install_efk(params: dict, namespace: str = 'cluster-tools'):
    """
    Installs EFK to the current kubernetes environment.

    :param params: a dictionary containing the params to insert into the efk chart's values.yaml
    :param namespace: the namespace to install efk in. defaults to cluster-tools
    :return: True on success, exception if failure.
    """

    set_default_namespace(namespace)
    if not namespace_exists(namespace):
        create_namespace(namespace)

    ns_ls = helm_ls(namespace)
    # install chart
    helm_install('simoncomputing/efk', params, release_name = 'efk', values_path = abs_path('yaml/efk-values.yml'), namespace = namespace)
    # get pod
    time.sleep(1)
    pods = list_pods(namespace)
    elastic_pod = False
    for p in pods:
        if p.get('name', '').find('elasticsearch') != -1:
            elastic_pod = p.get('name', False)
    # wait for pod to be ready
    if not wait_for_pod(elastic_pod, namespace, timeout = 300):
        raise('Elastic pod did not ready within 5 minutes. Please verify that your params are complete and correct.')

    for p in pods:
        if p.get('name', '').find('kibana') != -1:
            kibana_pod = p.get('name', False)
    # wait for pod to be ready
    if not wait_for_pod(kibana_pod, namespace, timeout = 300):
        raise('Kibana pod did not ready within 5 minutes. Please verify that your params are complete and correct.')

    return True

def install_sonarqube(params: dict, namespace: str = 'cluster_tools'):
    """
    Installs SonarQube to the current kubernetes environment.

    :param params: a dictionary containing the params to insert into the sonarqube chart's values.yaml
    :param namespace: the namespace to install sonarqube in. defaults to cluster-tools
    :return: True on success, exception if failure.
    """
    # install chart
    # get pod
    # wait for pod to be ready
    set_default_namespace(namespace)
    if not namespace_exists(namespace):
        create_namespace(namespace)

    ns_ls = helm_ls(namespace)
    # install chart
    helm_install('simoncomputing/sonarqube', params, release_name = 'efk', values_path = abs_path('yaml/sonarqube-values.yml'), namespace = namespace)
    # get pod
    time.sleep(1)
    pods = list_pods(namespace)
    sonar_pod = False
    for p in pods:
        if p.get('name', '').find('sonar') != -1:
            sonar_pod = p.get('name', False)
    # wait for pod to be ready
    if not wait_for_pod(sonar_pod, namespace, timeout = 300):
        raise('Sonar pod did not ready within 5 minutes. Please verify that your params are complete and correct.')
    return True

def install_prometheus(params: dict, namespace: str = 'cluster_tools'):
    """
    Installs Prometheus to the current kubernetes environment.

    :param params: a dictionary containing the params to insert into the prometheus chart's values.yaml
    :param namespace: the namespace to install prometheus in. defaults to cluster-tools
    :return: True on success, exception if failure.
    """
    # install chart
    # get pod
    # wait for pod to be ready
    set_default_namespace(namespace)
    if not namespace_exists(namespace):
        create_namespace(namespace)

    ns_ls = helm_ls(namespace)
    # install chart
    helm_install('simoncomputing/prometheus', params, release_name = 'prometheus', values_path = abs_path('yaml/prometheus-values.yml'), namespace = namespace)
    # get pod
    time.sleep(1)
    pods = list_pods(namespace)
    prom_pod = False
    for p in pods:
        if p.get('name', '').find('prometheus') != -1:
            prom_pod = p.get('name', False)
    # wait for pod to be ready
    if not wait_for_pod(prom_pod, namespace, timeout = 300):
        raise('Prometheus pod did not ready within 5 minutes. Please verify that your params are complete and correct.')
    return True

def install_grafana(params: dict, namespace: str = 'cluster_tools'):
    """
    Installs grafana to the current kubernetes environment.

    :param params: a dictionary containing the params to insert into the grafana chart's values.yaml
    :param namespace: the namespace to install grafana in. defaults to cluster-tools
    :return: True on success, exception if failure.
    """
    # install chart
    # get pod
    # wait for pod to be ready
    set_default_namespace(namespace)
    if not namespace_exists(namespace):
        create_namespace(namespace)

    ns_ls = helm_ls(namespace)
    # install chart
    helm_install('simoncomputing/grafana', params, release_name = 'grafana', values_path = abs_path('yaml/grafana-values.yml'), namespace = namespace)
    # get pod
    time.sleep(1)
    pods = list_pods(namespace)
    grafana_pod = False
    for p in pods:
        if p.get('name', '').find('grafana') != -1:
            grafana_pod = p.get('name', False)
    # wait for pod to be ready
    if not wait_for_pod(grafana_pod, namespace, timeout = 300):
        raise('Grafana pod did not ready within 5 minutes. Please verify that your params are complete and correct.')
    return True

def install_cluster_tools(params: dict, namespace: str = 'cluster_tools'):
    """
    Installs all cluster tools to the current kubernetes environment. Does not install cicd tools.

    :param params: a dictionary containing the params to insert into the grafana chart's values.yaml
    :param namespace: the namespace to install all cluster tools in. defaults to cluster-tools
    :return: True on success, exception if failure.
    """

    install_prometheus(params, namespace)
    install_grafana(params, namespace)
    install_efk(params, namespace)

    