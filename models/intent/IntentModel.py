import tensorflow as tf
from tensorflow.keras.models import Model, load_model
from tensorflow.keras import preprocessing


# 의도 분류 모델 모듈
class IntentModel:
    def __init__(self, model_name, preprocess):

        # 의도 클래스 별 레이블
        self.labels = {0: "상품주문", 1: "할인적용문의", 2: "상품색상문의", 3: "반품요청", 4: "상품가격문의", 5:'주문취소요청' , 6:'상품사이즈문의', 7: '배송일정확인' , 8: '상품추천요청',9:'주문수량확인' ,10:'카테고리선택',11:'긍정',12:'부정',13:'기타'}

        # 의도 분류 모델 불러오기
        self.model = load_model(model_name)

        # 챗봇 Preprocess 객체
        self.p = preprocess


    # 의도 클래스 예측
    def predict_class(self, query):
        # 형태소 분석
        pos = self.p.pos(query)

        # 문장내 키워드 추출(불용어 제거)
        keywords = self.p.get_keywords(pos, without_tag=True)
        sequences = [self.p.get_wordidx_sequence(keywords)]

        # 단어 시퀀스 벡터 크기
        from config.GlobalParams import MAX_SEQ_LEN

        # 패딩처리
        padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen=MAX_SEQ_LEN, padding='post')

        predict = self.model.predict(padded_seqs)
        predict_class = tf.math.argmax(predict, axis=1)
        return predict_class.numpy()[0]
