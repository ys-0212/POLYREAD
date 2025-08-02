from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

model = AutoModelForSequenceClassification.from_pretrained("model")

tokenizer = AutoTokenizer.from_pretrained("model")

clf = pipeline("text-classification", model=model, tokenizer=tokenizer)
def language_detection(text):


    result = clf(text)

    return result

if __name__ == "__main__":
    sample_text = "落子共黄十任七日敢萬 西城頭如射山消朗月苦思 恭税区务书河上神明宰 为心自開熟為 进 少人谓城的 思鱼知兄弟登马過 马容各佳節倍 馬岛 多少年相逢意氣馬无做 新美消斗十子成阳侠 杯消西出陶坐故人言"
    result = language_detection(sample_text)
    print(f"Detected Language: {result[0]['label']} with score {result[0]['score']:.2f}")