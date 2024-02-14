import React from 'react';

function AboutPage() {
  return (
    <div className="text-left bg-gray-100 px-12 sm:px-20 pb-12">
      <h2 className="text-3xl text-center font-bold">About Us</h2>

      <h5 className="text-xl font-bold mt-8">
        <strong>The Edge Predictor</strong>
      </h5>

      <p className="text-xs sm:text-sm mt-2">
        Welcome to The Edge Predictor, your premier destination for unlocking the
        secrets of sporting events through cutting-edge computer-based data
        analysis and algorithms. At The Edge Predictor, we've harnessed the
        power of technology to give you the winning edge in the world of sports
        betting.
      </p>

      <h5 className="text-lg font-bold mt-8">
        <strong>Our Mission</strong>
      </h5>

      <p className="text-xs sm:text-sm mt-2">
        At The Edge Predictor, our mission is to revolutionize the way you
        approach sports betting. We're dedicated to providing you with accurate,
        data-driven predictions that empower you to make informed betting
        decisions. We believe in leveling the playing field and giving you the
        advantage you deserve.
      </p>

      <h5 className="text-lg font-bold mt-8">
        <strong>The Power of Algorithms</strong>
      </h5>

      <p className="text-xs sm:text-sm mt-2">
        Our team of expert data scientists and sports enthusiasts has developed
        state-of-the-art algorithms that crunch vast amounts of data from
        various sporting events. These algorithms analyze historical data,
        player statistics, team performance, and more to generate predictions
        that are as close to a sure bet as you can get.
      </p>

      <h5 className="text-lg font-bold mt-8">
        <strong>Why Choose The Edge Predictor?</strong>
      </h5>

      <div className="grid grid-cols-1 px-2 sm:grid-cols-5 sm:pb-0">
        <div className="text-xs sm:text-sm mt-2"> 
          <span className="font-bold">Accuracy:</span> Our algorithms are
          constantly fine-tuned to deliver the most accurate predictions,
          increasing your chances of winning.
        </div>
        <div className="text-xs sm:text-sm mt-2">
          <span className="font-bold">Transparency:</span> We believe in
          transparency and provide you with the reasoning behind each
          prediction, so you can trust our recommendations.
        </div>
        <div className="text-xs sm:text-sm mt-2">
          <span className="font-bold">Diverse Sports Coverage:</span> From
          football to basketball, soccer to tennis, we cover a wide range of
          sports, ensuring you never miss an opportunity to win big.
        </div>
        <div className="text-xs sm:text-sm mt-2">
          <span className="font-bold">User-Friendly Interface:</span> Our
          website is designed with you in mind, offering an intuitive and
          user-friendly experience to make your betting journey enjoyable.
        </div>
        <div className="text-xs sm:text-sm mt-2">
          <span className="font-bold">Responsible Gaming:</span> We prioritize
          responsible gaming and encourage our users to gamble responsibly,
          ensuring a safe and enjoyable experience.
        </div>
      </div>

      <h5 className="text-lg font-bold mt-8">
        <strong>Join Us Today</strong>
      </h5>

      <p className="text-xs sm:text-sm mt-2">
        Discover the future of sports betting with The Edge Predictor. Whether
        you're a seasoned bettor or new to the game, we're here to guide you
        toward success. Join us today and take the first step towards maximizing
        your winnings with the help of data-driven predictions.
      </p>

      <p className="text-xs sm:text-sm mt-2">
        With The Edge Predictor, you're not just betting; you're betting smart.
      </p>
    </div>
  );
}

export default AboutPage;