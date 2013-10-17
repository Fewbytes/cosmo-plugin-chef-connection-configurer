#/*******************************************************************************
# * Copyright (c) 2013 GigaSpaces Technologies Ltd. All rights reserved
# *
# * Licensed under the Apache License, Version 2.0 (the "License");
# * you may not use this file except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *       http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.
# *******************************************************************************/

"""
Celery tasks for running recipes through chef-client.

This file implements the connection configurer interface, where for each of tasks, we check that chef is
configured
and run the relevant runlist using the chef_client module.
"""


from cosmo.events import send_event, get_cosmo_properties
from cosmo.celery import celery
from chef_client_common.chef_client import set_up_chef_client, run_chef


@celery.task
@set_up_chef_client
@celery.task
def configure_connection(__source_cloudify_id,
                         __target_cloudify_id,
                         __source_properties,
                         __target_properties,
                         **kwargs):
    chef_configure_connection_runlist = __source_properties['chef_configure_connection_runlist']
    target_ip = __source_properties['cloudify_runtime'][__target_cloudify_id]['ip']
    chef_attributes = __source_properties['chef_attributes']
    chef_attributes['injected'] = {
        'mezzanine_db_host': target_ip
    }
    run_chef(chef_configure_connection_runlist, chef_attributes)


@celery.task
def configure_connection(__source_cloudify_id,
                         __target_cloudify_id,
                         __source_properties,
                         __target_properties,
                         **kwargs):
    chef_unconfigure_connection_runlist = __source_properties['chef_unconfigure_connection_runlist']
    chef_attributes = __source_properties['__source_cloudify_id']
    run_chef(chef_unconfigure_connection_runlist, chef_attributes)
