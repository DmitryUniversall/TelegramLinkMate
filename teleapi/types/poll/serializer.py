from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from teleapi.core.orm.serializers.generics.fields import RelatedSerializerField, ListSerializerField, StringSerializerField
from teleapi.types.message_entity import MessageEntitySerializer
from .sub_object.option import PollOptionSerializer
from .obj import Poll


class PollSerializer(ModelSerializer):
    type_ = StringSerializerField(read_name='type')
    options = ListSerializerField(RelatedSerializerField(PollOptionSerializer()))
    explanation_entities = ListSerializerField(RelatedSerializerField(MessageEntitySerializer()), is_required=False)

    class Meta:
        model = Poll
