import React from 'react';
import PropTypes from 'prop-types';

class Likes extends React.Component {
  /* Display number of image and post owner of a single post
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = { numLikes: 0, lognameLiked: 0 };
    this.handleLike = this.handleLike.bind(this);
    this.handleUnlike = this.handleUnlike.bind(this);
  }

  componentDidMount() {
    this.getRequest();
  }

  handleLike() {
    // event.preventDefault();
    // console.log('clicked');
    const { url } = this.props;
    // const { numLikes, lognameLiked } = this.state;
    fetch(url, {
      credentials: 'same-origin',
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    })
      .then(() => {
        // can we just use likeres here instead of a prev state????
        // ?
        // ?
        this.setState((addLike) => ({
          numLikes: parseInt(addLike.numLikes, 10) + 1,
          lognameLiked: 1,
        }));
        // this.componentDidMount();
      })
      .catch((error) => console.log(error));
  }

  handleUnlike() {
    // event.preventDefault();
    const { url } = this.props;
    // const { numLikes, lognameLiked } = this.state;
    fetch(url, {
      credentials: 'same-origin',
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
    })
      .then(() => {
        this.setState((deleteLike) => ({
          numLikes: parseInt(deleteLike.numLikes, 10) - 1,
          lognameLiked: 0,
        }));
        // this.componentDidMount();
      })
      .catch((error) => console.log(error));
  }

  getRequest() {
    const { url } = this.props;
    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // console.log(`data_post:${data}`);
        this.setState({
          numLikes: data.likes_count,
          lognameLiked: data.logname_likes_this,
        });
      })
      .catch((error) => console.log(error));
  }

  render() {
    // This line automatically assigns this.state.imgUrl to the const variable imgUrl
    // and this.state.owner to the const variable owner
    const { numLikes, lognameLiked } = this.state;
    // const { url } = this.props;

    let numLikesDisplay;
    if (numLikes === 1) {
      numLikesDisplay = (
        <p>
          {' '}
          {numLikes}
          {' '}
          like
          {' '}
        </p>
      );
    } else {
      numLikesDisplay = (
        <p>
          {' '}
          {numLikes}
          {' '}
          likes
          {' '}
        </p>
      );
    }

    let typeButton;
    if (!lognameLiked) {
      // console.log("two");
      typeButton = (
        <button className="like-unlike-button" type="submit" onClick={this.handleLike}>
          like
        </button>
      );
    } else {
      // console.log("three");
      typeButton = (
        <button className="like-unlike-button" type="submit" onClick={this.handleUnlike}>
          unlike
        </button>
      );
    }

    // console.log("isdl"+this.props.isDoubleLiked)

    return (
      <div>
        {numLikesDisplay}
        {typeButton}
      </div>
    );
  }
}

Likes.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Likes;
