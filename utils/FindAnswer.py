class FindAnswer:
    
    # Database 인스턴스 객체로 생성
    def __init__(self, db):
        self.db = db    # 이 객체를 통해 답변을 검색
        
    # ② 답변 검색
    # 의도명(intent_name) 과 개체명 태그 리스트(ner_tags) 를 이용해 질문의 답변을 검색
    def search(self, intent_name, ner_tags):
        from config.now_state import now_state
        # 의도명, 개체명으로 답변 검색
        sql = self._make_query(intent_name, ner_tags)
        answer = self.db.select_one(sql)
        
        # 검색되는 답변이 없었으면 의도명만 이용하여 답변 검색
        # 챗봇이 찾는 정확한 조건의 답변이 없는 경우 차선책으로 동일한 의도를 가지는 답변을 검색
        # (의도가 동일한 경우 답변도 유사할 확률이 높다!)      
        if answer is None:
            sql = self._make_query(intent_name, None)
            answer = self.db.select_one(sql)
        
        r_answer = answer['answer']

        print(f"현재 state: {now_state.state}") 
        if now_state.state == 0:
            if now_state.flag == False:    
                if intent_name == '상품추천요청':
                    if ner_tags and ('B_CATEGORY' in ner_tags):
                        self.change_state(1)
                    else:
                        self.change_state(2)
                elif intent_name == '할인적용문의':
                    self.change_state(10)
                elif intent_name == '반품요청':
                    self.change_state(8)
                elif intent_name == '주문취소요청':
                    self.change_state(9)
                elif intent_name == '배송일정확인':
                    self.change_state(0)
                
        if now_state.state == 1:
            if now_state.flag == False: 
                if intent_name == '상품주문':
                    self.change_state(6)
                elif intent_name == '할인적용문의':
                    self.change_state(10)
                elif intent_name == '상품색상문의':
                    self.change_state(5)
                elif intent_name == '반품요청':
                    self.change_state(8)
                elif intent_name == '상품가격문의':
                    self.change_state(3)
                elif intent_name == '주문취소요청':
                    self.change_state(9)
                elif intent_name == '상품사이즈문의':
                    self.change_state(4)
                elif intent_name == '배송일정확인':
                    self.change_state(0)
                elif intent_name == '상품추천요청':
                    if ner_tags == None:
                        self.change_state(2)
                    elif 'B_CATEGORY' in ner_tags:
                        self.change_state(1)
                    else:
                        self.change_state(2)
                    
        if now_state.state == 2:
            if now_state.flag == False:
                if intent_name and ner_tags and ('B_CATEGORY' in ner_tags):
                    self.change_state(1)
                
        if now_state.state == 3:
            if now_state.flag == False:
                self.change_state(1)
                # if intent_name == '긍정':
        #             self.change_state(6)
        #         elif intent_name == '부정':
        #             self.change_state(1)
        #         elif intent_name == '상품추천요청':
        #             if 'B_CATEGORY' in ner_tags:
        #                 self.change_state(1)
        #             else:
        #                 self.change_state(2)
        
        if now_state.state == 4:
            if now_state.flag == False:
                self.change_state(1)
        #     if now_state.flag == False:
        #         if intent_name == '긍정':
        #             self.change_state(6)
        #         elif intent_name == '부정':
        #             self.change_state(1)
        #         elif intent_name == '상품추천요청':
        #             if 'B_CATEGORY' in ner_tags:
        #                 self.change_state(1)
        #             else:
        #                 self.change_state(2)
        
        if now_state.state == 5:
            if now_state.flag == False:
                self.change_state(1)
        #     if now_state.flag == False:
        #         if intent_name == '긍정':
        #             self.change_state(6)
        #         elif intent_name == '부정':
        #             self.change_state(1)
        #         elif intent_name == '상품추천요청':
        #             if 'B_CATEGORY' in ner_tags:
        #                 self.change_state(1)
        #             else:
        #                 self.change_state(2)
                
        if now_state.state == 6:
            if (now_state.flag == False) and (intent_name == '주문수량확인'):
                self.change_state(7)
        
        if now_state.state == 8: # 반품
            if now_state.flag == False:
                if intent_name == '긍정':
                    self.change_state(11)
                elif intent_name == '부정':
                    self.change_state(0)
                    r_answer = '이용해주셔서 감사합니다.💖<br> 문의사항이  있으시면 언제든 말씀 해주세요.'
        
        if now_state.state == 9: # 주문취소
            if now_state.flag == False:
                if intent_name == '긍정':
                    self.change_state(12)
                elif intent_name == '부정':
                    self.change_state(0)
                    r_answer = '이용해주셔서 감사합니다.💖<br> 문의사항이  있으시면 언제든 말씀 해주세요.'
                
        if now_state.state == 10:
            if now_state.flag == False:
                if intent_name == '긍정':
                    self.change_state(2)
                elif intent_name == "부정":
                    self.change_state(0)
                   
        if now_state.flag == False:
            r_answer = '지금은 입력할 수 없는 값입니다. 처음으로 돌아갑니다.'
            now_state.state = 0
        
        now_state.flag = False
            
        # 0: 처음
        # 1: 추천받을 물품이 전역변수에 저장되어 있는 상황.
        # 2: 추천해달라고 했으나 핵심어 누락으로 카테고리를 입력받아야 하는 상황
        # 3: 해당 상품은 __원입니다. 주문 도와드릴까요? 라고 답변하는 상황
        # 4: 상품 사이즈는 다음과 같아요. ___. 주문 도와드릴까요? 라고 답변하는 상황
        # 5: 상품 색상은 다음과 같아요. ___. 주문 도와드릴까요? 라고 답변하는 상황
        # 6: 고객이 주문하고 싶다고 하여 고객에게 색상, 사이즈, 수량을 버튼으로 입력하라고 하는 상황
        # 7: x
        # 8: ____ 상품에 대해 반품 요청하시는 게 맞으신가요? 라고 답변하는 상황
        # 9: ____ 상품에 대해 주문 취소 요청하시는 게 맞으신가요? 라고 답변하는 상황
        # 10: 고객님의 ?% 쿠폰을 쓰면 할인 받을 수 있습니다. 고객님 취향에 맞는 상품을 추천해드릴까요? 라고 답변하는 상황.
        print(f"바뀐 state: {now_state.state}") 

        return (r_answer, answer['answer_image'])
    
    # ③ 검색 쿼리 생성
    # '의도명' 만 검색할지, 여러종류의 개체명 태그와 함께 검색할지 결정하는 '조건'을 만드는 간단한 함수
    def _make_query(self, intent_name, ner_tags):
        sql = "select * from chatbot_qa_data"
        if intent_name != None and ner_tags == None:
            sql = sql + " where intent='{}' ".format(intent_name)
            sql += 'and ner IS NULL'

        elif intent_name != None and ner_tags != None:
            where = ' where intent="%s" ' % intent_name
            if (len(ner_tags) > 0):
                where += 'and ('
                for ne in ner_tags:
                    where += " ner like '%{}%' or ".format(ne)
                where = where[:-3] + ')'
            sql = sql + where    
            
        # 동일한 답변이 2개 이상인 경우 랜덤으로 선택
        sql = sql + " order by rand() limit 1"
        return sql
    
    # ④ NER 태그를 실제 입력된 단어로 변환
    
    # 예를 들어 '자장명 주문할께요' 라는 텍스트가 챗본 엔진에 입력되었다고 합시다.
    # 그러면 챗봇 엔진은 '자장명'을 'B_FOOD 객체명'으로 인식합니다.
    # 이때 검색된 답변이 '{B_FOOD} 주문 처리 완료 되었습니다 주문해주셔서 감사합니다' 라고 한다면,
    # 답변 내용속 '{B_FOOD}' 를 '자장면' 으로 변환해 주는 함수입니다.
    # 변환해야 하는 태그가 더 존재한다면 변환 규칙을 추가하면 됩니다.
    
    def tag_to_word(self, ner_predicts, answer):
        # for word, tag in ner_predicts:

        #     # 변환해야하는 태그가 있는 경우 추가
        #     if tag == 'B_FOOD' or tag == 'B_DT' or tag == 'B_TI':
        #         answer = answer.replace(tag, word)

#         answer = answer.replace('{', '')
#         answer = answer.replace('}', '')
        
        if (answer == "고객님의 취향에 맞춰 골라봤어요. ,"):
            import numpy as np
            import pandas as pd
            from config.ProductName import ProductName
            
            for word, tag in ner_predicts:
                if tag == "B_CATEGORY":
                    temp1 = word
                    temp = {"신발": '0', "바지": '1', "스니커즈": '2', "상의": '3', "스포츠/용품": '4', "시계": '5',
                    "여성": '6', "가방": '7', "아우터": '8', "모자": '9', "액세서리": '10', "주얼리": '11', 
                        "책/음악/티켓": '12', "뷰티": '13', "스커트": '14', "생활/취미/예술": '15',
                    "양말/레그웨어": '16', "속옷": '17', "원피스": '18', "선글라스/안경테": '19', "반려동물": '20'}
                    try:
                        r = pd.read_excel(f"C:/TeamProject_/TeamProj2/catagory/category_{temp[temp1]}.xlsx")[:50].T[:50].T
                    except:
                        # 잘못된 카테고리가 입력되면
                        ProductName.name = "" # 상품 이름 변수를 null string으로 바꾸고
                        raise Exception('잘못된 카테고리 입력됨.')
                
                    R = r.values
                    my_ratings = r.values[-1]
                    Where_NaN = np.argwhere(np.isnan(my_ratings)).ravel()
                    
                    min_ = 100
                    Theta, X = self.initialize(R, 10)  # 행렬들 초기화
                    Theta, X, costs = self.gradient_descent(R, Theta, X, 100, 0.0007, 0.01)
                    Good_Theta, Good_X, Good_costs = Theta, X, costs
                        
                    max_rating = 0
                    max_rating_index = -1
                    predict_metrix = Good_Theta @ Good_X
                    for i in Where_NaN:
                        if predict_metrix[-1][i] > max_rating:
                            max_rating = predict_metrix[-1][i]
                            max_rating_index = i
                    
                    # answer += f"\n {r.columns[max_rating_index]}"
                    ProductName.name = r.columns[max_rating_index]
                    answer = '고객님의 취향에 맞춰 골라봤어요. '
        return answer 
    
    def loss(self, prediction, R): # 손실 함수
        import numpy as np
        return np.nansum((prediction - R)**2)


    def initialize(self, R, num_features): # 랜덤으로 2개의 행렬 생성.
        import numpy as np
        num_users, num_items = R.shape

        Theta = np.random.rand(num_users, num_features)
        X = np.random.rand(num_features, num_items)

        return Theta, X


    def gradient_descent(self, R, Theta, X, iteration, alpha, lambda_): # 경사 하강법.
        import numpy as np
        num_user, num_items = R.shape
        num_features = len(X)
        costs = []

        for _ in range(iteration):
            prediction = Theta @ X
            error = prediction - R
            costs.append(self.loss(prediction, R))

            for i in range(num_user):
                for j in range(num_items):
                    if not np.isnan(R[i][j]):
                        for k in range(num_features):
                            Theta[i][k] -= alpha * (np.nansum(error[i, :]*X[k, :]) + lambda_*Theta[i][k])
                            X[k][j] -= alpha * (np.nansum(error[:, j]*Theta[:, k]) + lambda_*X[k][j])

        return Theta, X, costs

    def change_state(self, num):
        from config.now_state import now_state
        now_state.state = num
        now_state.flag = True