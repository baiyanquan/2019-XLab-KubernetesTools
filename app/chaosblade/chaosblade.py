from flask import Blueprint, jsonify
from flask import request
from flask import abort
from services.fault_injector import FaultInjector
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from services.k8s_observer import K8sObserver
from services.message_queue import RabbitMq

chaosblade = Blueprint('chaosblade', __name__)


@chaosblade.route('/tool/api/v1.0/chaosblade/inject-cpu', methods=['POST'])
def chaos_inject_cpu():
    if not request.json or 'host' not in request.json or 'timeout' not in request.json:
        abort(400)
    mq_control = RabbitMq.control()
    dto = {
        'host': request.json['host'],
        'timeout': request.json['timeout'],
        'open': mq_control
    }
    return jsonify(FaultInjector.chaos_inject_cpu(dto))


@chaosblade.route('/tool/api/v1.0/chaosblade/inject-random/with_time', methods=['POST'])
def chaos_inject_cpu_with_time():
    if not request.json or 'host' not in request.json or 'second' not in request.json:
        abort(400)
    mq_control = RabbitMq.control()
    dto_time = {
        'time': request.json['second']
    }
    dto = {
        'host': request.json['host'],
        'open': mq_control
    }
    scheduler = BackgroundScheduler()
    now = datetime.now()
    delta = timedelta(seconds=int(dto_time['time'].encode('raw_unicode_escape')))
    scheduler.add_job(func=lambda: FaultInjector.chaos_inject_random(dto), trigger='date', next_run_time=(now + delta))
    scheduler.start()
    time.sleep(delta.total_seconds() + 1)
    return "success"


@chaosblade.route('/tool/api/v1.0/chaosblade/inject-mem', methods=['POST'])
def chaos_inject_mem():
    if not request.json or 'host' not in request.json or 'percent' not in request.json or 'timeout' not in request.json:
        abort(400)
    mq_control = RabbitMq.control()
    dto = {
        'host': request.json['host'],
        'percent': request.json['percent'],
        'timeout': request.json['timeout'],
        'open': mq_control
    }
    return jsonify(FaultInjector.chaos_inject_mem(dto))


@chaosblade.route('/tool/api/v1.0/chaosblade/inject-disk', methods=['POST'])
def chaos_inject_disk():
    if not request.json or 'host' not in request.json or 'type' not in request.json or 'timeout' not in request.json:
        abort(400)
    mq_control = RabbitMq.control()
    dto = {
        'host': request.json['host'],
        'type': request.json['type'],
        'timeout': request.json['timeout'],
        'open': mq_control
    }
    return jsonify(FaultInjector.chaos_inject_disk(dto))


@chaosblade.route('/tool/api/v1.0/chaosblade/inject-network', methods=['POST'])
def chaos_inject_network():
    if not request.json or 'host' not in request.json or 'time' not in request.json or 'timeout' not in request.json:
        abort(400)
    mq_control = RabbitMq.control()
    dto = {
        'host': request.json['host'],
        'time': request.json['time'],
        'timeout': request.json['timeout'],
        'open': mq_control
    }
    return jsonify(FaultInjector.chaos_inject_network(dto))


@chaosblade.route('/tool/api/v1.0/chaosblade/inject-random', methods=['POST'])
def chaos_inject_random():
    if not request.json or 'host' not in request.json or 'timeout' not in request.json:
        abort(400)
    mq_control = RabbitMq.control()
    dto = {
        'host': request.json['host'],
        'timeout': request.json['timeout'],
        'open': mq_control
    }
    return jsonify(FaultInjector.chaos_inject_random(dto))


@chaosblade.route('/tool/api/v1.0/chaosblade/inject-pod-single', methods=['POST'])
def chaos_inject_pod_single():
    if not request.json or 'host' not in request.json or 'pod' not in request.json or \
            'timeout' not in request.json:
        abort(400)
    mq_control = RabbitMq.control()
    dto = {
        'host': request.json['host'],
        'pod': request.json['pod'],
        'timeout': request.json['timeout'],
        'open': mq_control
    }
    return jsonify(FaultInjector.chaos_inject_pod_single(dto))


@chaosblade.route('/tool/api/v1.0/chaosblade/stop-specific-inject', methods=['POST'])
def stop_specific_inject():
    if not request.json or 'tag' not in request.json:
        abort(400)
    mq_control = RabbitMq.control()
    dto = {
        'tag': request.json['tag'],
        'open': mq_control
    }
    return jsonify(FaultInjector.stop_specific_chaos_inject(dto))


@chaosblade.route('/tool/api/v1.0/chaosblade/stop-all-inject-on-specific-node', methods=['POST'])
def stop_all_inject():
    if not request.json or 'host' not in request.json:
        abort(400)
    mq_control = RabbitMq.control()
    dto = {
        'host': request.json['host'],
        'open': mq_control
    }
    return jsonify(FaultInjector.stop_all_on_specific_node(dto))


@chaosblade.route('/tool/api/v1.0/chaosblade/stop-all-inject-on-all-nodes', methods=['POST'])
def stop_all_inject_on_all_nodes():
    mq_control = RabbitMq.control()
    mq_control = {
        'open': mq_control
    }
    return jsonify(FaultInjector.stop_all_chaos_inject_on_all_nodes(mq_control))


@chaosblade.route('/tool/api/v1.0/chaosblade/view-inject-info', methods=['GET'])
def view_inject_info():
    return jsonify(FaultInjector.view_chaos_inject())


@chaosblade.route('/tool/api/v1.0/chaosblade/view-inject-on-host-by-status', methods=['POST'])
def view_all_create_success_inject_info():
    if not request.json or 'host' not in request.json or 'status' not in request.json:
        abort(400)
    status = str(request.json['status']).capitalize()
    if status not in ['Success', 'Destroyed', 'Error']:
        abort(400)
    dto = {
        'host': request.json['host'],
        'status': request.json['status']
    }
    return jsonify(FaultInjector.view_inject_on_host_by_status(dto))


@chaosblade.route('/tool/api/v1.0/chaosblade/delete-specific-service', methods=['POST'])
def delete_specific_kind_pods():
    if not request.json or 'service' not in request.json:
        abort(400)
    mq_control = RabbitMq.control()
    dto = {
        'service': request.json['service'],
        'open': mq_control
    }
    print dto
    return jsonify(FaultInjector.delete_all_pods_for_service(dto))


@chaosblade.route('/tool/api/v1.0/chaosblade/get-service-log', methods=['POST'])
def get_pod_log():
    if not request.json or 'service' not in request.json or 'namespace' not in request.json:
        abort(400)
    pod_name = request.json['service']
    namespace = request.json['namespace']
    return jsonify(K8sObserver.get_service_log(pod_name, namespace))


@chaosblade.route('/tool/api/v1.0/chaosblade/test-config-default-cmd', methods=['GET'])
def test_config():
    return jsonify(FaultInjector.test_config())
