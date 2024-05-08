from run import got_solve_text
from tasks.text import init_Task_by_string # 导入任务类


# 定义推理模块
class Reasoning:
    feedback: str=None
    def call(self, problem_description: str, profile_type_prompt: str=None, LLM_type: list = ['gpt-3.5-turbo'], feedback: str = None) -> str:
        reasoning_results = thought_propagation(problem_description) #调用对应推理模块得到结果
        # 比如 reasoning_results =  reasoning_self_refine(problem_description: str,
        # profile_type_prompt: str = None, LLM_type: list[str] = ['gpt-3.5-turbo'], feedback: str = None) -> str:
        self.feedback = None #与环境交互，更新feedback
        
        return reasoning_results


# 核心是通过类比获得其他问题，聚合各个问题的答案以获得最终答案
def thought_propagation(problem_description: str, profile_type_prompt: str = None,
                        LLM_type: list = ['gpt-3.5-turbo']) -> str:
    """
    profile_type_prompt: file中存取任务
    """

    #初始化任务类（便于清洗格式）
    task = init_Task_by_string(problem_description)

    # 得到答案和推理过程
    _ , _,final_message = got_solve_text(task, 0)    #设置原论文中idx=0，因为是单任务
    answer = final_message.split('Passage:\n')[-1]

    return answer


class Agent():

    name: str 
    profile: str 
    memory: None
    env: None
    reasoning: Reasoning = Reasoning()
    tooluse: None
    planning: None





#测试agent
thought_propagation_agent = Agent()
#输入文本，使其续写
#推广到其他任务可修改prompts/text中的prompt
task="It isn't difficult to do a handstand if you just stand on your hands. "
#运行需要一段时间
#thought_propagation(problem_description=task)
result=thought_propagation_agent.reasoning.call(problem_description=task)
print(result)


