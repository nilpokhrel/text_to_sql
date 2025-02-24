import instructions
import llm_manager

llm_engine = llm_manager.LLMManager()

class Agents:
    @classmethod
    def user_query_explorer(cls, user_query):
        detailed_query = llm_engine.query_engine(user_query, system_response_query=instructions.user_query_exploration)
        return detailed_query
    
    @classmethod
    def user_query_to_sql(cls, explored_user_query):
        sql_query = llm_engine.query_engine(explored_user_query, system_response_query=instructions.user_query_to_sql.format(instructions.flight_context))
        return sql_query
    
    @classmethod
    def combined_sql_generation(cls, user_query):
        sql_query = llm_engine.query_engine(user_query, system_response_query=instructions.combined_instruction)
        return sql_query
    
    @classmethod
    def flight_agent(cls, natural_user_query):
        user_intent = cls.user_query_explorer(natural_user_query)
        print('user intent: ',user_intent)
        sql_query = cls.user_query_to_sql(user_intent)
        print('sql:  ',sql_query)
        return sql_query
    
if __name__ == '__main__':
    # q = 'I need to get all airline list that moves from us to nepal.'
    # print(Agents.flight_agent(q))
    pass