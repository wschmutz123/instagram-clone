import React from 'react';
import PropTypes from 'prop-types';
import * as moment from 'moment';
import Likes from './likes';
import Comment from './comment';

class Post extends React.Component {
  /* Display number of image and post owner of a single post
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = {
      imgUrl: '', owner: '', ownerShowUrl: '', postShowUrl: '', ownerImgUrl: '',
    };
    this.handleImgLike = this.handleImgLike.bind(this);
    this.likesRef = React.createRef();
  }

  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    this.getRequest();
  }

  componentDidUpdate(prevProps) {
    // Typical usage (don't forget to compare props):
    const { url } = this.props;
    if (url !== prevProps.url) {
      this.getRequest();
    }
  }

  handleImgLike() {
    if (this.likesRef.current.state.lognameLiked === 0) {
      this.likesRef.current.handleLike();
    }
  }

  getRequest() {
    const { url } = this.props;

    // Call REST API to get the post's information
    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
      //  console.log(data);
        this.setState({
          imgUrl: data.img_url,
          owner: data.owner,
          //      age: data.age,
          ownerShowUrl: data.owner_show_url,
          postShowUrl: data.post_show_url,
          ownerImgUrl: data.owner_img_url,
        });
      })
      .catch((error) => console.log(error));
  }

  render() {
    // This line automatically assigns this.state.imgUrl to the const variable imgUrl
    // and this.state.owner to the const variable owner
    const {
      imgUrl, owner, ownerShowUrl, postShowUrl, ownerImgUrl,
    } = this.state;
    const { url } = this.props;
    let { commentUrl } = '';
    let { likeUrl } = '';

    commentUrl = `${url}comments/`;
    likeUrl = `${url}likes/`;

    const time = new Date();
    const timestamp = moment(time, 'YYYYMMDD').fromNow();

    // Render number of post image and post owner
    return (
      <div className="post">
        <p>
          {' '}
          <a href={ownerShowUrl}>
            {' '}
            <img src={ownerImgUrl} className="userphoto" alt="post" />
            {owner}
            {' '}
          </a>
        </p>
        <p>
          {' '}
          <a href={postShowUrl}>{timestamp}</a>
          {' '}
        </p>
        <img src={imgUrl} onDoubleClick={this.handleImgLike} className="center" alt="post" />
        <Likes url={likeUrl} ref={this.likesRef} />
        <Comment url={commentUrl} />
      </div>
    );
  }
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Post;
