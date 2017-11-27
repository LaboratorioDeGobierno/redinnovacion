from base.tests import BaseTestCase
from comments.models import Comment, MENTION_DELIMITER

from users.models import User


class CommentTest(BaseTestCase):
    def setUp(self):
        super(CommentTest, self).setUp()
        self.user1 = self.create_user(
            status=User.STATUS_ACCEPTED,
        )
        self.user2 = self.create_user(
            status=User.STATUS_ACCEPTED,
        )
        self.users = (self.user1, self.user2)

    def test_get_parsed_content(self):
        """
        Tests Comment.get_parsed_content expecting it to change slugs with ids
        """
        content = (u"{delimiter}{user1}, this is test comment mentioning "
                   u"you and {delimiter}{user2}")
        original = content.format(
            delimiter=MENTION_DELIMITER,
            user1=self.user1.slug,
            user2=self.user2.slug,
        )
        expected = content.format(
            delimiter=MENTION_DELIMITER,
            user1=self.user1.id,
            user2=self.user2.id,
        )

        text = Comment.get_parsed_content(original, self.users)
        self.assertEqual(text, expected)
