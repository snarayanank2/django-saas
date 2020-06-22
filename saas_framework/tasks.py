import logging
from saas_framework.core.workspaces.models import Workspace

logger = logging.getLogger(__name__)

def workspace_summary(workspace_id):
    logger.info('printing details of workspace %s', workspace_id)
    workspace = Workspace.objects.get(id=workspace_id)
    logger.info('workspace %s', workspace)