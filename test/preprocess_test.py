from utils.Preprocess import Preprocess

sent = "이 바지 다른 색상 있나요?"

p = Preprocess(userdic='../utils/train.tvs')

pos = p.pos(sent)

ret = p.get_keywords(pos, without_tag=False)
print(ret)

ret = p.get_keywords(pos, without_tag=True)
print(ret)