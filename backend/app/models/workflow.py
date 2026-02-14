from sqlalchemy import Column, String, Integer, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from app.db.base import BaseModel


class WorkflowDefinition(BaseModel):
    """
    工作流定义模型类
    
    用于定义各种业务流程的审批流程
    工作流定义描述了流程的各个步骤、审批人、审批规则等
    通过配置JSON可以实现灵活的流程定制
    """
    __tablename__ = "workflow_definitions"
    
    name = Column(String(100), nullable=False, comment="流程名称")
    code = Column(String(50), unique=True, index=True, comment="流程编码")
    type = Column(String(50), comment="流程类型：purchase/sale/payment/other")
    description = Column(Text, comment="描述")
    status = Column(Integer, default=1, comment="状态")
    config = Column(JSON, comment="流程配置JSON")
    
    instances = relationship("WorkflowInstance", back_populates="definition")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "type": self.type,
            "description": self.description,
            "status": self.status,
            "config": self.config,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class WorkflowInstance(BaseModel):
    """
    工作流实例模型类
    
    用于记录工作流的实际执行过程
    每次发起一个业务审批时，都会创建一个工作流实例
    实例跟踪流程的当前状态、当前步骤等
    """
    __tablename__ = "workflow_instances"
    
    code = Column(String(50), unique=True, index=True, nullable=False, comment="实例编号")
    definition_id = Column(Integer, ForeignKey("workflow_definitions.id"), nullable=False, comment="流程定义ID")
    business_type = Column(String(50), comment="业务类型")
    business_id = Column(Integer, comment="业务ID")
    current_step = Column(String(50), comment="当前步骤")
    status = Column(String(20), default="pending", comment="状态：pending/approved/rejected/cancelled")
    initiator_id = Column(Integer, ForeignKey("users.id"), comment="发起人")
    remark = Column(Text, comment="备注")
    
    definition = relationship("WorkflowDefinition", back_populates="instances")
    initiator = relationship("User")
    logs = relationship("WorkflowLog", back_populates="instance", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "definition_id": self.definition_id,
            "business_type": self.business_type,
            "business_id": self.business_id,
            "current_step": self.current_step,
            "status": self.status,
            "initiator_id": self.initiator_id,
            "remark": self.remark,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class WorkflowLog(BaseModel):
    """
    工作流日志模型类
    
    用于记录工作流的审批历史
    每次审批操作都会产生一条日志记录
    日志记录了审批人、审批意见、审批时间等信息，方便追溯
    """
    __tablename__ = "workflow_logs"
    
    instance_id = Column(Integer, ForeignKey("workflow_instances.id", ondelete="CASCADE"), nullable=False, comment="实例ID")
    step_name = Column(String(50), comment="步骤名称")
    action = Column(String(20), comment="操作：submit/approve/reject/cancel")
    handler_id = Column(Integer, ForeignKey("users.id"), comment="处理人")
    comment = Column(Text, comment="审批意见")
    
    instance = relationship("WorkflowInstance", back_populates="logs")
    handler = relationship("User")
    
    def to_dict(self):
        return {
            "id": self.id,
            "instance_id": self.instance_id,
            "step_name": self.step_name,
            "action": self.action,
            "handler_id": self.handler_id,
            "comment": self.comment,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
