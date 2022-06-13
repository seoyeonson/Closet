class FindAnswer:
    
    # Database 인스턴스 객체로 생성
    def __init__(self, db):
        self.db = db    # 이 객체를 통해 답변을 검색
        
    # ② 답변 검색
    # 의도명(intent_name) 과 개체명 태그 리스트(ner_tags) 를 이용해 질문의 답변을 검색
    def search(self, intent_name, ner_tags):  
        # 의도명, 개체명으로 답변 검색
        sql = self._make_query(intent_name, ner_tags)
        answer = self.db.select_one(sql)
        
        # 검색되는 답변이 없었으면 의도명만 이용하여 답변 검색
        # 챗봇이 찾는 정확한 조건의 답변이 없는 경우 차선책으로 동일한 의도를 가지는 답변을 검색
        # (의도가 동일한 경우 답변도 유사할 확률이 높다!)      
        if answer is None:
            sql = self._make_query(intent_name, None)
            answer = self.db.select_one(sql)
            
        return (answer['answer'], answer['answer_image'])
    
    # ③ 검색 쿼리 생성
    # '의도명' 만 검색할지, 여러종류의 개체명 태그와 함께 검색할지 결정하는 '조건'을 만드는 간단한 함수
    def _make_query(self, intent_name, ner_tags):
        sql = "select * from chatbot_qa_data"
        if intent_name != None and ner_tags == None:
            sql = sql + " where intent='{}' ".format(intent_name)

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

        answer = answer.replace('{', '')
        answer = answer.replace('}', '')
        
        if (answer == "고객님의 취향에 맞춰 골라봤어요. ,"):
            import numpy as np
            import pandas as pd
            from config.ProductName import ProductName
            
            for word, tag in ner_predicts:
                if tag == "B_CATEGORY":
                    temp1 = word
                    break
            temp = {"신발": '0', "바지": '1', "스니커즈": '2', "상의": '3', "스포츠/용품": '4', "시계": '5',
                   "여성": '6', "가방": '7', "아우터": '8', "모자": '9', "액세서리": '10', "주얼리": '11', 
                    "책/음악/티켓": '12', "뷰티": '13', "스커트": '14', "생활/취미/예술": '15',
                   "양말/레그웨어": '16', "속옷": '17', "원피스": '18', "선글라스/안경테": '19', "반려동물": '20'}
            r = pd.read_excel(f"D:/DevRoot/new/TeamProj2/catagory/category_{temp[temp1]}.xlsx")[:50].T[:50].T
            R = r.values
            my_ratings = r.values[-1]
            Where_NaN = np.argwhere(np.isnan(my_ratings)).ravel()
            
            min_ = 100
            Theta, X = self.initialize(R, 10)  # 행렬들 초기화
            Theta, X, costs = self.gradient_descent(R, Theta, X, 100, 0.0007, 0.01)
            # if min_ > costs[-1] and costs[-1] != 0:
            #     min_ = costs[-1]
            Good_Theta, Good_X, Good_costs = Theta, X, costs
                
            max_rating = 0
            max_rating_index = -1
            predict_metrix = Good_Theta @ Good_X
            for i in Where_NaN:
                if predict_metrix[-1][i] > max_rating:
                    max_rating = predict_metrix[-1][i]
                    max_rating_index = i
                    
            answer += f"\n {r.columns[max_rating_index]}"
            ProductName.name = r.columns[max_rating_index]
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